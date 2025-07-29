# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------

import json
from typing import Annotated, Literal

import pandas as pd
from pydantic import Field

from ibm_watsonx_gov.config import AgenticAIConfiguration, GenAIConfiguration
from ibm_watsonx_gov.entities.enums import TaskType
from ibm_watsonx_gov.entities.evaluation_result import (AggregateMetricResult,
                                                        RecordMetricResult)
from ibm_watsonx_gov.entities.metric import GenAIMetric, MetricThreshold
from ibm_watsonx_gov.metrics.tool_calling_hallucination.static_evaluation import \
    static_evaluate_calls
from ibm_watsonx_gov.utils.python_utils import parse_functions_to_schema

TOOL_CALLING_HALLUCINATION = "tool_calling_hallucination"
TCH_METHODS = ["static_evaluator"]


class ToolCallingHallucinationMetric(GenAIMetric):
    """
    Implementation class for ToolCallingHallucinationMetric.

    The following methods are supported:
    1. static_evaluator
    """

    name: Annotated[Literal["tool_calling_hallucination"], Field(title="Metric Name",
                                                                 description="The name of metric.",
                                                                 default=TOOL_CALLING_HALLUCINATION)]
    tasks: Annotated[list[TaskType], Field(title="Task Type",
                                           description="The generative task type.",
                                           default=[TaskType.RAG])]
    thresholds: Annotated[list[MetricThreshold], Field(title="Metric threshold",
                                                       description="Value that defines the violation limit for the metric",
                                                       default=[MetricThreshold(
                                                           type="upper_limit", value=0.7)]
                                                       )]
    method: Annotated[Literal["static_evaluator"], Field(title="Computation Method",
                                                         description="The method used to compute the metric.",
                                                         default="static_evaluator")]

    def evaluate(self, data: pd.DataFrame | dict,
                 configuration: GenAIConfiguration | AgenticAIConfiguration,
                 **kwargs) -> AggregateMetricResult:
        """
        Evaluate the data for Tool Call Hallucinations
        Args:
            data (pd.DataFrame | dict): Data to be evaluated
            configuration (GenAIConfiguration | AgenticAIConfiguration): Metrics configuration

        Returns:
            AggregateMetricResult: The computed metrics
        """

        # Validate the configuration to compute the TCH
        self.__validate_configuration(data, configuration)

        # Pre-process the data for the TCH Computation
        data = self.__pre_process(data, configuration)

        # Compute the metrics
        metric_result = self.__compute_metrics(
            data, configuration=configuration)

        # Post process to make the aggregated and record level metrics results
        metric_result = self.__post_process(metric_result, configuration)

        return metric_result

    def __validate_configuration(self, data: pd.DataFrame, configuration: GenAIConfiguration | AgenticAIConfiguration) -> None:
        """
        Validate the configuration to compute the tch metrics
        """
        if self.method not in TCH_METHODS:
            raise ValueError(
                f"The provided method '{self.method}' for computing '{self.name}' metric is not supported.")
        if not configuration.tools:
            raise ValueError(
                f"The tools list is missing for computing '{self.name}'.")
        if not configuration.tool_calls_field:
            raise ValueError(
                f"The tool_call_field is required to compute the '{self.name}'")

    def __pre_process(self, data: pd.DataFrame, configuration: GenAIConfiguration | AgenticAIConfiguration):
        """
        Preprocess the dataframe and tool list for metrics computation

        Args:
            data (pd.DataFrame): Input dataframe

        Returns:
            pd.Dataframe: Processed dataframe
        """
        # Get the specification of tools used in the application
        # in proper format if it is a list of Callable
        if isinstance(configuration.tools, list) and all(callable(item) for item in configuration.tools):
            configuration.tools = self.__get_tools_list_schema(
                configuration.tools)

        # TODO: Add validation for the tool_call_field data schema
        tool_call_field = configuration.tool_calls_field
        if tool_call_field:
            data[tool_call_field] = data[tool_call_field].apply(
                lambda x: json.loads(x) if isinstance(x, str) else x)
        return data

    def __get_tools_list_schema(self, tools: list) -> list:
        """
        Convert the list of callable objects to the 
        format needed for the TCH computation

        Args:
            tools (list): List of Callable objects

        Returns:
            list: List of dictionary containing the tool
            specifications
        """
        tools_specifications = []
        for func in tools:
            tool_schema = parse_functions_to_schema(func)
            if not tool_schema:
                continue
            tools_specifications.append(tool_schema)

        return tools_specifications

    def __compute_metrics(self, data: pd.DataFrame, configuration: GenAIConfiguration | AgenticAIConfiguration):
        """
        Compute the TCH metrics for the given data

        Args:
            data (pd.DataFrame): Input data including the tools used for the application
            configuration (GenAIConfiguration | AgenticAIConfiguration): Metrics configuration

        Raises:
            Exception: When the computation is failed

        Returns:
            list: List of metrics calculated for each records
        """

        try:
            question_field = configuration.question_field
            tool_calls_field = configuration.tool_calls_field
            record_id_field = configuration.record_id_field
            record_level_metrics = []

            for _, row in data.iterrows():

                # The data could be a list of json or an
                # AI message response, if it is an AI message
                # extract the tool calls from the AI message response
                tool_calls_response = row[tool_calls_field]
                if not isinstance(tool_calls_response, list):
                    tool_calls = tool_calls_response.tool_calls if hasattr(
                        tool_calls_response, 'tool_calls') else []
                    tool_calls_response = [{
                        "name": call['name'],
                        "parameters": call['args']
                    } for call in tool_calls]

                # Compute the static evaluation metrics
                explanations = static_evaluate_calls(tool_specifications=configuration.tools,
                                                     query=row[question_field], tool_calls=tool_calls_response)
                record_level_metrics.append({
                    "value": 1.0 if explanations else 0.0,
                    "record_id": row[record_id_field],
                    "explanations": explanations or []
                })
            return record_level_metrics
        except Exception as ex:
            raise Exception(
                f"Error while computing metrics: '{self.name}' using '{self.method}'. Reason: {str(ex)}")

    def __post_process(self, results: pd.DataFrame, configuration: GenAIConfiguration | AgenticAIConfiguration):
        """
        Post process the computed metrics to get the Aggregated Result and
        Record level metric result in the proper format

        Args:
            results (pd.DataFrame): Computed metric results
            configuration (GenAIConfiguration | AgenticAIConfiguration): Metric configuration

        Returns:
            AggregateMetricResult: The AggregateMetricResult object containing the calculated
            metrics information
        """

        # Preparing the record level metrics
        record_level_metrics: list[RecordMetricResult] = []

        for row in results:
            record_level_metrics.append(
                RecordMetricResult(
                    name=TOOL_CALLING_HALLUCINATION,
                    method=self.method,
                    value=row.get("value"),
                    provider="TOOL_CALLING_HALLUCINATION",
                    record_id=row.get(configuration.record_id_field),
                    additional_info={"explanations": row.get("explanations")}
                )
            )

        # Get the number of records are violated, min, max
        values = [item.get("value", 0.0) for item in results]
        count_invalid = sum(val == 1.0 for val in values)
        min_value = min(values, default=0.0)
        max_value = max(values, default=0.0)
        value = int(count_invalid)/int(len(results))

        # creating AggregateMetricResult
        aggregated_result = AggregateMetricResult(
            name=TOOL_CALLING_HALLUCINATION,
            method=self.method,
            provider="TOOL_CALLING_HALLUCINATION",
            value=value,
            total_records=len(results),
            record_level_metrics=record_level_metrics,
            min=min_value,
            max=max_value

        )

        # return the aggregated result
        return aggregated_result
