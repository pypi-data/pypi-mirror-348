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

from ibm_watsonx_gov.config import AgenticAIConfiguration, GenAIConfiguration
from ibm_watsonx_gov.entities.enums import MetricGroup, TaskType
from ibm_watsonx_gov.entities.evaluation_result import AggregateMetricResult
from ibm_watsonx_gov.entities.llm_judge import LLMJudge
from ibm_watsonx_gov.entities.metric import GenAIMetric, MetricThreshold
from ibm_watsonx_gov.providers.unitxt_provider import (UnitxtColumnMapping,
                                                       UnitxtProvider)

ANSWER_RELEVANCE = "answer_relevance"
UNITXT_METRIC_NAME = ANSWER_RELEVANCE
unitxt_methods = [
    "token_recall",
    "llm_as_judge",
]


class AnswerRelevanceMetric(GenAIMetric):
    name: Annotated[Literal["answer_relevance"],
                    Field(default=ANSWER_RELEVANCE)]
    tasks: Annotated[list[TaskType], Field(
        default=[TaskType.RAG])]
    thresholds: Annotated[list[MetricThreshold], Field(default=[MetricThreshold(
        type="lower_limit", value=0.7)])]
    method: Annotated[
        Literal["token_recall", "llm_as_judge"],
        Field(description="The method used to compute the metric. This field is optional and when `llm_judge` is provided, the method would be set to `llm_as_judge`.",
              default="token_recall")]
    group: Annotated[MetricGroup, Field(
        default=MetricGroup.ANSWER_QUALITY, frozen=True)]
    llm_judge: Annotated[LLMJudge | None, Field(
        description="The LLM judge used to compute the metric.", default=None)]

    @model_validator(mode="after")
    def set_llm_judge_default_method(self) -> Self:
        # If llm_judge is set, set the method to llm_as_judge
        if self.llm_judge:
            self.method = "llm_as_judge"
        return self

    def evaluate(self, data: pd.DataFrame | dict,
                 configuration: GenAIConfiguration | AgenticAIConfiguration,
                 **kwargs) -> AggregateMetricResult:
        if self.method not in unitxt_methods:
            raise ValueError(
                f"The provided method '{self.method}' for computing '{self.name}' metric is not supported.")

        if self.method == "llm_as_judge" and not self.llm_judge and not configuration.llm_judge:
            raise ValueError(
                f"llm_judge is required for computing {self.name} using {self.method} method")

        # Define the mapping if the method is not using the default one
        if self.method == "token_recall":
            column_mapping = UnitxtColumnMapping(
                answer="prediction/answer",
                question="task_data/question",
            )
        else:
            column_mapping = UnitxtColumnMapping()

        provider = UnitxtProvider(
            configuration=configuration,
            metric_name=self.name,
            metric_method=self.method,
            metric_prefix="metrics.rag.external_rag",
            metric_alias=UNITXT_METRIC_NAME,
            metric_group=self.group,
            column_mapping=column_mapping,
            llm_judge=self.llm_judge,
            **kwargs,
        )
        aggregated_metric_result = provider.evaluate(data=data)

        return aggregated_metric_result
