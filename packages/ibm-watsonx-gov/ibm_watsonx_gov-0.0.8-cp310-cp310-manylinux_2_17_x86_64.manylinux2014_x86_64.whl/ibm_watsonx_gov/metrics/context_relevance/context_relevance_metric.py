# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------

from typing import Annotated, Literal

import pandas as pd
from pydantic import Field, model_validator
from typing_extensions import Self

from ibm_watsonx_gov.config.gen_ai_configuration import GenAIConfiguration
from ibm_watsonx_gov.entities.enums import (EvaluationProvider, MetricGroup,
                                            TaskType)
from ibm_watsonx_gov.entities.evaluation_result import (AggregateMetricResult,
                                                        RecordMetricResult)
from ibm_watsonx_gov.entities.llm_judge import LLMJudge
from ibm_watsonx_gov.entities.metric import GenAIMetric, MetricThreshold
from ibm_watsonx_gov.providers import UnitxtProvider
from ibm_watsonx_gov.utils.python_utils import transform_str_to_list

CONTEXT_RELEVANCE = "context_relevance"


class ContextRelevanceResult(RecordMetricResult):
    name: str = CONTEXT_RELEVANCE
    group: MetricGroup = MetricGroup.RETRIEVAL_QUALITY
    additional_info: dict[Literal["contexts_values"],
                          list[float]] = {"context_values": []}


unitxt_methods = [
    "sentence_bert_bge",
    "sentence_bert_mini_lm",
    "llm_as_judge",
]


class ContextRelevanceMetric(GenAIMetric):
    name: Annotated[Literal["context_relevance"],
                    Field(default=CONTEXT_RELEVANCE)]
    tasks: Annotated[list[TaskType], Field(
        default=[TaskType.RAG])]
    thresholds: Annotated[list[MetricThreshold], Field(default=[MetricThreshold(
        type="lower_limit", value=0.7)])]
    method: Annotated[
        Literal["sentence_bert_bge", "sentence_bert_mini_lm",
                "llm_as_judge"],
        Field(description="The method used to compute the metric. This field is optional and when `llm_judge` is provided, the method would be set to `llm_as_judge`.",
              default="sentence_bert_mini_lm")]
    group: Annotated[MetricGroup, Field(
        default=MetricGroup.RETRIEVAL_QUALITY, frozen=True)]
    llm_judge: Annotated[LLMJudge | None, Field(
        description="The LLM judge used to compute the metric.", default=None)]

    @model_validator(mode="after")
    def set_llm_judge_default_method(self) -> Self:
        # If llm_judge is set, set the method to llm_as_judge
        if self.llm_judge:
            self.method = "llm_as_judge"
        return self

    def evaluate(self, data: pd.DataFrame | dict, configuration: GenAIConfiguration, **kwargs) -> AggregateMetricResult:
        if self.method not in unitxt_methods:
            raise ValueError(
                f"The provided method '{self.method}' for computing '{self.name}' metric is not supported.")

        if self.method == "llm_as_judge" and not self.llm_judge and not configuration.llm_judge:
            raise ValueError(
                f"llm_judge is required for computing {self.name} using {self.method} method")

        context_fields = configuration.context_fields

        # Check if we need to expand the contexts column:
        if len(configuration.context_fields) == 1:
            context = context_fields[0]
            data[context] = data[context].apply(transform_str_to_list)
            contexts_count = len(data[context].iloc[0])
            context_fields = [f"context_{i}" for i in range(contexts_count)]
            data[context_fields] = pd.DataFrame(
                data[context].to_list(), index=data.index)

        contexts_result: list[AggregateMetricResult] = []
        for context in context_fields:
            context_config = configuration.model_copy()
            context_config.context_fields = [context]
            context_provider = UnitxtProvider(
                configuration=context_config,
                metric_name=self.name,
                metric_method=self.method,
                metric_group=self.group,
                metric_prefix="metrics.rag.external_rag",
                llm_judge=self.llm_judge,
                **kwargs
            )
            res = context_provider.evaluate(data=data)
            contexts_result.append(res)

        final_res: list[ContextRelevanceResult] = []
        for record_metric in zip(*[context_result.record_level_metrics for context_result in contexts_result]):
            values = [context_value.value for context_value in record_metric]
            record_result = ContextRelevanceResult(
                method=self.method,
                provider=EvaluationProvider.UNITXT.value,
                value=max(values),
                record_id=record_metric[0].record_id,
                additional_info={"contexts_values": values},
            )
            final_res.append(record_result)

        # Create the aggregate result
        values = [record.value for record in final_res]
        mean = sum(values) / len(values)
        aggregate_result = AggregateMetricResult(
            name=self.name,
            method=self.method,
            provider=EvaluationProvider.UNITXT.value,
            group=MetricGroup.RETRIEVAL_QUALITY,
            value=mean,
            total_records=len(final_res),
            record_level_metrics=final_res,
            min=min(values),
            max=max(values),
            mean=mean,
        )

        return aggregate_result
