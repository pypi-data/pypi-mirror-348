# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------

import pandas as pd
from pydantic import Field, PrivateAttr
from typing_extensions import Annotated

from ibm_watsonx_gov.config.gen_ai_configuration import GenAIConfiguration
from ibm_watsonx_gov.entities.enums import MetricGroup
from ibm_watsonx_gov.entities.evaluation_result import MetricsEvaluationResult
from ibm_watsonx_gov.entities.metric import GenAIMetric
from ibm_watsonx_gov.evaluators.base_evaluator import BaseEvaluator
from ibm_watsonx_gov.visualizations import ModelInsights, display_table


class MetricsEvaluator(BaseEvaluator):
    """
    The class to evaluate the metrics and display the results.

    Examples:
        1. Basic usage
            .. code-block:: python

                config = GenAIConfiguration(input_fields=["context", "question"],
                                    question_field="question",
                                    context_fields=["context"],
                                    output_fields=["generated_text"],
                                    reference_fields=["reference_answer"])
                wxgov_client = APIClient(credentials=Credentials(api_key=""))
                evaluator = MetricsEvaluator(configuration=config, api_client=wxgov_client)

                metrics = [AnswerSimilarityMetric()]
                df = pd.read_csv("")
                result = evaluator.evaluate(data=df, metrics=metrics)

                # Get the results in the required format
                result.to_json()
                result.to_df()
                result.to_dict()

                # Display the results
                evaluator.display_table()
                evaluator.display_insights()

        2. Using specifying metrics group
            .. code-block:: python

                metrics = [AnswerSimilarityMetric()]
                metric_groups = [MetricGroup.RETRIEVAL_QUALITY]
                df = pd.read_csv("")
                result = evaluator.evaluate(data=df, metrics=metrics,metric_groups=metric_groups)
    """
    configuration: Annotated[GenAIConfiguration,
                             Field(name="The configuration for metrics evaluation.")]
    _data: Annotated[pd.DataFrame | dict | None,
                     PrivateAttr(default=None)]
    _metrics: Annotated[list[GenAIMetric] | None,
                        PrivateAttr(default=None)]
    _metric_groups: Annotated[list[MetricGroup] | None,
                              PrivateAttr(default=None)]
    _result: Annotated[MetricsEvaluationResult | None,
                       PrivateAttr(default=None)]

    def evaluate(
            self,
            data: pd.DataFrame | dict,
            metrics: list[GenAIMetric] = [],
            metric_groups: list[MetricGroup] = [],
            **kwargs) -> MetricsEvaluationResult:
        """
        Evaluate the metrics for the given data.

        Args:
            data (pd.DataFrame | dict): The data to be evaluated.
            metrics (list[GenAIMetric], optional): The metrics to be evaluated. Defaults to [].
            metric_groups (list[MetricGroup], optional): The metric groups to be evaluated. Defaults to [].
            **kwargs: Additional keyword arguments.

        Returns:
            MetricsEvaluationResult: The result of the evaluation.
        """
        from ..evaluate.impl.evaluate_metrics_impl import (
            _evaluate_metrics, _resolve_metric_dependencies)
        self._data = data
        self._metrics = _resolve_metric_dependencies(
            metrics=metrics, metric_groups=metric_groups)
        self._metric_groups = metric_groups,
        self._result: MetricsEvaluationResult = _evaluate_metrics(configuration=self.configuration,
                                                                  data=data,
                                                                  metrics=self._metrics,
                                                                  api_client=self.api_client,
                                                                  **kwargs)
        return self._result

    def display_table(self):
        """
        Display the metrics result as a table.
        """
        display_table(self._result.to_df(data=self._data))

    def display_insights(self):
        """
        Display the metrics result in a venn diagram based on the metrics threshold.
        """
        model_insights = ModelInsights(
            configuration=self.configuration, metrics=self._metrics)
        model_insights.display_metrics(
            metrics_result=self._result.to_df(data=self._data))
