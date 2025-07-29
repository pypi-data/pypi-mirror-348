# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------


from abc import abstractmethod
from typing import TYPE_CHECKING, Annotated, Literal

import pandas as pd
from pydantic import BaseModel, Field, computed_field

from ibm_watsonx_gov.entities.base_classes import BaseMetric
from ibm_watsonx_gov.entities.enums import MetricGroup, TaskType
from ibm_watsonx_gov.entities.evaluation_result import AggregateMetricResult

if TYPE_CHECKING:
    from ibm_watsonx_gov.config import (AgenticAIConfiguration,
                                        GenAIConfiguration)


class MetricThreshold(BaseModel):
    """
    The class that defines the threshold for a metric.
    """
    type: Annotated[Literal["lower_limit", "upper_limit"], Field(
        description="Threshold type. One of 'lower_limit', 'upper_limit'")]
    value: Annotated[float, Field(
        title="Threshold value", description="The value of metric threshold", default=0)]


class Locale(BaseModel):
    input: list[str] | dict[str, str] | str | None = None
    output: list[str] | None = None
    reference: list[str] | dict[str, str] | str | None = None


class GenAIMetric(BaseMetric):
    """Defines the Generative AI metric interface"""
    thresholds: Annotated[list[MetricThreshold],
                          Field(description="The list of thresholds", default=[])]
    tasks: Annotated[list[TaskType], Field(
        description="The task types this metric is associated with.", frozen=True)]
    group: Annotated[MetricGroup | None, Field(
        description="The metric group this metric belongs to.", frozen=True, default=None)]
    is_reference_free: Annotated[bool, Field(
        description="Decides whether this metric needs a reference for computation", frozen=True, default=True)]
    method: Annotated[
        str | None,
        Field(description="The method used to compute the metric.",
              default=None)]
    metric_dependencies: Annotated[list[BaseMetric], Field(
        description="Metrics that needs to be evaluated first", default=[])]

    @computed_field(return_type=str)
    @property
    def id(self):
        if self._id is None:
            self._id = self.name + (f"_{self.method}" if self.method else "")
        return self._id

    @abstractmethod
    def evaluate(self, data: pd.DataFrame | dict,
                 configuration: "GenAIConfiguration | AgenticAIConfiguration",
                 **kwargs) -> AggregateMetricResult:
        raise NotImplementedError

    def info(self):
        pass


class PredictiveAIMetric(BaseMetric):
    pass
