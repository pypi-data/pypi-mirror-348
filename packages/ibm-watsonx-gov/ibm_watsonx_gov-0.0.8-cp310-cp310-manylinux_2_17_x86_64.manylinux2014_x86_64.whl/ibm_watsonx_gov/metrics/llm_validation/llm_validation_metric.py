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
from pydantic import Field

from ibm_watsonx_gov.config import AgenticAIConfiguration, GenAIConfiguration
from ibm_watsonx_gov.entities.enums import TaskType
from ibm_watsonx_gov.entities.evaluation_result import AggregateMetricResult
from ibm_watsonx_gov.entities.llm_judge import LLMJudge
from ibm_watsonx_gov.entities.metric import GenAIMetric, MetricThreshold

LLMValidation = "llm_validation"


class LLMValidationMetric(GenAIMetric):
    """Defines the implementation for computing the LLMValidation metric.

    .. code-block:: python

        from ibm_watsonx_gov.entities.foundation_model import WxAIFoundationModel
        wx_ai_provider = WxAIModelProvider(
            credentials=WxAICredentials(url="https://us-south.ml.cloud.ibm.com", api_key="api_key1")
        )
        evaluator = WxAIFoundationModel(
            model_name="model_name1",
            project_id="project_id1",
            model_id="model_id1",
            provider=wx_ai_provider,
        )
        metric = LLMValidationMetric(ai_evaluator=evaluator)

    .. code-block:: python

        from ibm_watsonx_gov.entities.foundation_model import CustomFoundationModel
        evaluator = CustomFoundationModel(
            model_name="model_name1", scoring_fn=scoring_fn
        )
        threshold  = MetricThreshold(type="lower_limit", value=0.5)
        metric = LLMValidationMetric(ai_evaluator=evaluator, threshold=threshold)
    """
    name: Annotated[Literal["llm_validation"],
                    Field(default=LLMValidation)]
    tasks: Annotated[list[TaskType], Field(
        default=[TaskType.RAG, TaskType.SUMMARIZATION])]
    thresholds: Annotated[list[MetricThreshold], Field(default=[MetricThreshold(
        type="lower_limit", value=0.7)])]
    method: Annotated[Literal["llm_as_judge"],
                      Field(description=f"The method used to compute the metric.",
                            default="llm_as_judge")]
    llm_judge: Annotated[LLMJudge | None, Field(
        description=f"The LLM judge used to compute the metric.")]

    def evaluate(self, data: pd.DataFrame | dict,
                 configuration: GenAIConfiguration | AgenticAIConfiguration,
                 **kwargs) -> AggregateMetricResult:

        # TODO Add implementation
        return
