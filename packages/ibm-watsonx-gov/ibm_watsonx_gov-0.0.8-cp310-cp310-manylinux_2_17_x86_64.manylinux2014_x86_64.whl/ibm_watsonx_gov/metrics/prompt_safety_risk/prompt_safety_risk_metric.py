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

from ibm_watsonx_gov.config.gen_ai_configuration import GenAIConfiguration
from ibm_watsonx_gov.entities.enums import MetricGroup, TaskType
from ibm_watsonx_gov.entities.evaluation_result import (AggregateMetricResult,
                                                        RecordMetricResult)
from ibm_watsonx_gov.entities.metric import GenAIMetric, MetricThreshold
from ibm_watsonx_gov.providers.detectors_provider import DetectorsProvider

PROMPT_SAFETY_RISK = "prompt_safety_risk"


class PromptSafetyRiskResult(RecordMetricResult):
    name: str = PROMPT_SAFETY_RISK
    group: MetricGroup = MetricGroup.CONTENT_SAFETY


prompt_safety_methods = ["prompt_injection_125m_0.7_en"]


class PromptSafetyRiskMetric(GenAIMetric):
    name: Annotated[Literal["prompt_safety_risk"],
                    Field(default=PROMPT_SAFETY_RISK)]
    method: Annotated[
        Literal["prompt_injection_125m_0.7_en"],
        Field(description=f"The method used to compute the prompt safety risk metric.",
              default="prompt_injection_125m_0.7_en")]
    thresholds: list[MetricThreshold] = [MetricThreshold(
        type="lower_limit", value=0.7)]
    tasks: Annotated[list[TaskType], Field(
        default=TaskType.values())]
    group: Annotated[MetricGroup, Field(
        default=MetricGroup.CONTENT_SAFETY, frozen=True)]

    def evaluate(
            self,
            data: pd.DataFrame | dict,
            configuration: GenAIConfiguration,
            **kwargs
    ) -> list[AggregateMetricResult]:

        if self.method not in prompt_safety_methods:
            raise ValueError(
                f"The provided method '{self.method}' for computing '{self.name}' metric is not supported.")
        provider = DetectorsProvider(configuration=configuration,
                                     metric_name=self.name,
                                     metric_method=self.method,
                                     metric_group=self.group,
                                     **kwargs)
        aggregated_metric_result = provider.evaluate(data=data)
        return aggregated_metric_result
