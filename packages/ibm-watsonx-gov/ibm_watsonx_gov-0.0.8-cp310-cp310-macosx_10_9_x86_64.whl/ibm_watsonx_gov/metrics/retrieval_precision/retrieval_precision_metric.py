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
from ibm_watsonx_gov.metrics.context_relevance.context_relevance_metric import (
    CONTEXT_RELEVANCE, ContextRelevanceMetric, ContextRelevanceResult)

RETRIEVAL_PRECISION = "retrieval_precision"


class RetrievalPrecisionResult(RecordMetricResult):
    name: str = RETRIEVAL_PRECISION
    group: MetricGroup = MetricGroup.RETRIEVAL_QUALITY


class RetrievalPrecisionMetric(GenAIMetric):
    name: Annotated[Literal["retrieval_precision"],
                    Field(default=RETRIEVAL_PRECISION)]
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
                relevance_scores=relevance_result.additional_info.get(
                    "contexts_values", []),
                threshold=self.thresholds[0].value,
            )
            scores.append(score)
            record_level_metrics.append(
                RetrievalPrecisionResult(
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

    def __compute(self, relevance_scores: list[float], threshold: float) -> float:
        relevance_list = []
        # Total Number of Contexts Retrieved
        total_no_of_contexts = len(relevance_scores)
        for r in relevance_scores:
            if r >= threshold:
                relevance_list.append(1)  # True positive
            else:
                relevance_list.append(0)  # False positive
        precision = sum(relevance_list) / \
            total_no_of_contexts if total_no_of_contexts > 0 else 0
        precision = round(precision, 4)
        return precision
