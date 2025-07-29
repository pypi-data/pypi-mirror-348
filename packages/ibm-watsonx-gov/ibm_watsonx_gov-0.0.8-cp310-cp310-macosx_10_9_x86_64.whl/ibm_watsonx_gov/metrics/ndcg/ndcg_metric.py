# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------


from typing import Annotated, Literal

import numpy as np
import pandas as pd
from pydantic import Field
from sklearn.metrics import ndcg_score

from ibm_watsonx_gov.config import AgenticAIConfiguration, GenAIConfiguration
from ibm_watsonx_gov.entities.enums import MetricGroup, TaskType
from ibm_watsonx_gov.entities.evaluation_result import (AggregateMetricResult,
                                                        RecordMetricResult)
from ibm_watsonx_gov.entities.metric import GenAIMetric, MetricThreshold
from ibm_watsonx_gov.metrics.context_relevance.context_relevance_metric import (
    CONTEXT_RELEVANCE, ContextRelevanceMetric, ContextRelevanceResult)

NDCG = "ndcg"


class NDCGResult(RecordMetricResult):
    name: str = NDCG
    group: MetricGroup = MetricGroup.RETRIEVAL_QUALITY


class NDCGMetric(GenAIMetric):
    name: Annotated[Literal["ndcg"],
                    Field(default=NDCG)]
    tasks: list[TaskType] = [TaskType.RAG]
    is_reference_free: bool = True
    thresholds: list[MetricThreshold] = [MetricThreshold(
        type="lower_limit", value=0.7)]
    metric_dependencies: list[GenAIMetric] = [ContextRelevanceMetric()]
    group: Annotated[MetricGroup, Field(
        default=MetricGroup.RETRIEVAL_QUALITY, frozen=True)]

    def evaluate(
            self,
            data: pd.DataFrame | dict,
            configuration: GenAIConfiguration | AgenticAIConfiguration,
            metrics_result: list[AggregateMetricResult],
            **kwargs,
    ) -> AggregateMetricResult:
        record_level_metrics = []
        scores = []

        context_relevance_result: list[ContextRelevanceResult] = next(
            (metric_result.record_level_metrics for metric_result in metrics_result if metric_result.name == CONTEXT_RELEVANCE), None)

        if context_relevance_result is None:
            raise Exception(
                f"Failed to evaluate {self.name} metric. Missing context relevance metric result")

        for relevance_result in context_relevance_result:
            score = self.__compute(
                relevance_result.additional_info.get(
                    "contexts_values", []),)
            scores.append(score)
            record_level_metrics.append(
                NDCGResult(
                    method="",
                    provider="",
                    record_id=relevance_result.record_id,
                    value=score,
                )
            )

        mean = sum(scores) / len(scores)
        aggregate_metric_score = AggregateMetricResult(
            name=self.name,
            method="",
            provider="",
            group=self.group,
            min=min(scores),
            max=max(scores),
            mean=mean,
            value=mean,
            total_records=len(record_level_metrics),
            record_level_metrics=record_level_metrics,
        )

        return aggregate_metric_score

    def __compute(self, relevance_scores: list[float]) -> float:
        if len(relevance_scores) < 2:
            return 1.0

        true_relevance = np.sort(relevance_scores)[::-1]

        ndcg_value = ndcg_score([true_relevance], [relevance_scores])

        return round(ndcg_value, 4)
