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
from ibm_watsonx_gov.entities.enums import MetricGroup, TaskType
from ibm_watsonx_gov.entities.evaluation_result import (AggregateMetricResult,
                                                        RecordMetricResult)
from ibm_watsonx_gov.entities.metric import GenAIMetric, MetricThreshold

UNSUCCESSFUL_REQUESTS = "unsuccessful_requests"


class UnsuccessfulRequestsResult(RecordMetricResult):
    name: str = UNSUCCESSFUL_REQUESTS
    group: MetricGroup = MetricGroup.ANSWER_QUALITY


class UnsuccessfulRequestsMetric(GenAIMetric):
    name: Annotated[Literal["unsuccessful_requests"],
                    Field(default=UNSUCCESSFUL_REQUESTS)]
    tasks: list[TaskType] = [TaskType.RAG]
    is_reference_free: bool = True
    thresholds: list[MetricThreshold] = [MetricThreshold(
        type="lower_limit", value=0.7)]
    unsuccessful_phrases: Annotated[list[str], Field(
        description="List of phrases to identify unsuccessful responses",
        examples=[["i do not know", "i am not sure"]],
        default=["i don't know", "i do not know", "i'm not sure",
                 "i am not sure", "i'm unsure", "i am unsure",
                 "i'm uncertain", "i am uncertain", "i'm not certain",
                 "i am not certain", "i can't fulfill", "i cannot fulfill"],
    )]
    group: Annotated[MetricGroup, Field(
        default=MetricGroup.ANSWER_QUALITY, frozen=True)]

    def evaluate(
            self,
            data: pd.DataFrame | dict,
            configuration: GenAIConfiguration | AgenticAIConfiguration,
            **kwargs
    ) -> AggregateMetricResult:
        record_level_metrics = []
        scores = []

        for prediction_field in configuration.output_fields:
            for prediction, record_id in zip(data[prediction_field], data[configuration.record_id_field]):
                value = 0
                for phrase in self.unsuccessful_phrases:
                    if phrase.lower() in prediction.lower():
                        value = 1
                        break
                scores.append(value)
                record_level_metrics.append(
                    UnsuccessfulRequestsResult(
                        method="",
                        provider="",
                        record_id=record_id,
                        value=value,
                    )
                )

        mean = sum(scores) / len(scores)
        aggregate_metric_score = AggregateMetricResult(
            name=self.name,
            method="",
            provider="",
            min=min(scores),
            max=max(scores),
            mean=mean,
            value=mean,
            total_records=len(record_level_metrics),
            group=self.group,
            record_level_metrics=record_level_metrics,
        )

        return aggregate_metric_score
