# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------


import uuid
from dataclasses import Field
from datetime import datetime
from typing import Annotated, Any, Literal, Optional

import pandas as pd
from pydantic import BaseModel, Field

from ibm_watsonx_gov.entities.base_classes import BaseMetricResult

AGENTIC_RESULT_COMPONENTS = Literal["conversation", "interaction", "node"]


class RecordMetricResult(BaseMetricResult):
    record_id: Annotated[str, Field(
        description="The record identifier.", examples=["record1"])]
    record_timestamp: Annotated[str | None, Field(
        description="The record timestamp.", examples=["2025-01-01T00:00:00.000000Z"], default=None)]


class ToolMetricResult(RecordMetricResult):
    tool_name: Annotated[str, Field(
        title="Tool Name", description="Name of the tool for which this result is computed.")]
    execution_count: Annotated[int, Field(
        title="Execution count", description="The execution count for this tool name.", gt=0, default=1)]

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ToolMetricResult):
            return False

        return (self.record_id, self.tool_name, self.execution_count, self.name, self.method, self.value, self.record_timestamp) == \
            (other.record_id, other.tool_name, other.execution_count,
             other.name, other.method, other.value, other.record_timestamp)

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, ToolMetricResult):
            raise NotImplemented

        return (self.record_id, self.tool_name, self.execution_count, self.name, self.method, self.value, self.record_timestamp) < \
            (other.record_id, other.tool_name, other.execution_count,
             other.name, other.method, other.value, other.record_timestamp)

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, ToolMetricResult):
            raise NotImplemented

        return (self.record_id, self.tool_name, self.execution_count, self.name, self.method, self.value, self.record_timestamp) > \
            (other.record_id, other.tool_name, other.execution_count,
             other.name, other.method, other.value, other.record_timestamp)

    def __le__(self, other: Any) -> bool:
        if not isinstance(other, ToolMetricResult):
            raise NotImplemented

        return (self.record_id, self.tool_name, self.execution_count, self.name, self.method, self.value, self.record_timestamp) <= \
            (other.record_id, other.tool_name, other.execution_count,
             other.name, other.method, other.value, other.record_timestamp)

    def __ge__(self, other: Any) -> bool:
        if not isinstance(other, ToolMetricResult):
            raise NotImplemented

        return (self.record_id, self.tool_name, self.execution_count, self.name, self.method, self.value, self.record_timestamp) >= \
            (other.record_id, other.tool_name, other.execution_count,
             other.name, other.method, other.value, other.record_timestamp)


class AggregateMetricResult(BaseMetricResult):
    min: float | None = None
    max: float | None = None
    mean: float | None = None
    total_records: int
    record_level_metrics: list[RecordMetricResult] = []


class MetricsEvaluationResult(BaseModel):
    metrics_result: list[AggregateMetricResult]

    def to_json(self, indent: int | None = None, **kwargs):
        """
        Transform the metrics evaluation result to a json.
        The kwargs are passed to the model_dump_json method of pydantic model. All the arguments supported by pydantic model_dump_json can be passed.

        Args:
            indent (int, optional): The indentation level for the json. Defaults to None.

        Returns:
            string of the result json.
        """
        if kwargs.get("exclude_unset") is None:
            kwargs["exclude_unset"] = True
        return self.model_dump_json(
            exclude={
                "metrics_result": {
                    "__all__": {
                        "record_level_metrics": {
                            "__all__": {"provider", "name", "method", "group"}
                        }
                    }
                }
            },
            indent=indent,
            **kwargs,
        )

    def to_df(self, data: pd.DataFrame | None = None) -> pd.DataFrame:
        """
        Transform the metrics evaluation result to a dataframe.

        Args:
            data (pd.DataFrame): the input dataframe, when passed will be concatenated to the metrics result

        Returns:
            pd.DataFrame: new dataframe of the input and the evaluated metrics
        """
        values_dict: dict[str, list[float | str | bool]] = {}
        for result in self.metrics_result:
            values_dict[f"{result.name}.{result.method}" if result.method else result.name] = [
                record_metric.value for record_metric in result.record_level_metrics]

        if data is None:
            return pd.DataFrame.from_dict(values_dict)
        else:
            return pd.concat([data, pd.DataFrame.from_dict(values_dict)], axis=1)

    def to_dict(self) -> list[dict]:
        """
        Transform the metrics evaluation result to a list of dict containing the record level metrics.
        """
        result = []
        for aggregate_metric_result in self.metrics_result:
            for record_level_metric_result in aggregate_metric_result.record_level_metrics:
                result.append(record_level_metric_result.model_dump())
        return result


class AgentMetricResult(BaseMetricResult):
    """
    This is the data model for metric results in the agentic app.
    It stores evaluation results for conversations, interactions and nodes.
    """
    id: Annotated[str, Field(
        description="The unique identifier for the metric result record. UUID.",
        default_factory=lambda: str(uuid.uuid4()))]

    ts: Annotated[datetime, Field(
        description="The timestamp when the metric was recorded.",
        default_factory=datetime.now)]

    applies_to: Annotated[AGENTIC_RESULT_COMPONENTS, Field(
        description="The type of component the metric result applies to.",
    )]

    interaction_id: Annotated[str | None, Field(
        description="The ID of the interaction being evaluated.")]

    interaction_ts: Annotated[datetime | None, Field(
        description="The timestamp of the interaction being evaluated.", default=None)]

    conversation_id: Annotated[str, Field(
        description="The ID of the conversation containing the interaction.", default=None)]

    node_name: Annotated[str | None, Field(
        description="The name of the node being evaluated.", default=None)]

    execution_count: Annotated[int | None, Field(
        title="Execution count", description="The execution count for this node name.", default=None)]


class AggregateAgentMetricResult(BaseMetricResult):
    min: Annotated[float | None, Field(
        description="The minimum value of the metric.", default=None)]
    max: Annotated[float | None, Field(
        description="The maximum value of the metric.", default=None)]
    mean: Annotated[float | None, Field(
        description="The mean value of the metric.", default=None)]
    value: Annotated[float | None, Field(
        description="The value of the metric. Defaults to mean.", default=None)]
    count: Annotated[int | None, Field(
        description="The count for metric results used for aggregation.", default=None)]
    node_name: Annotated[str | None, Field(
        description="The name of the node being evaluated.", default=None)]
    applies_to: Annotated[AGENTIC_RESULT_COMPONENTS, Field(
        description="The type of component the metric result applies to.",
    )]
    individual_results: Annotated[list[AgentMetricResult], Field(
        description="The list individual metric results.", default=[]
    )]


class AgenticEvaluationResult(BaseModel):
    metrics_result: list[AgentMetricResult]

    def get_aggregated_results(self, applies_to: AGENTIC_RESULT_COMPONENTS = ["conversation", "interaction", "node"], node_name: Optional[str] = None, include_individual_results: bool = False) -> list[AggregateAgentMetricResult]:
        """
        Get the agentic metrics aggregated results based on the specified arguments.

        Args:
            applies_to (AGENTIC_RESULT_COMPONENTS, optional): The type of component the metric result applies to. Defaults to ["conversation", "interaction", "node"].
            node_name (str, optional): The name of the node to get the aggregated results for. Defaults to None.
            individual_metrics (bool, optional): Whether to return the individual metrics results. Defaults to False.

        Return:
            returns: list[AggregateAgentMetricResult]
        """
        nodes_result_map = {}
        for mr in self.metrics_result:
            if node_name and mr.node_name != node_name:
                continue

            if mr.applies_to not in applies_to:
                continue

            key = mr.name+"."+mr.method if mr.method else mr.name
            if mr.node_name in nodes_result_map:
                if key in nodes_result_map[mr.node_name]:
                    nodes_result_map[mr.node_name][key].append(mr)
                else:
                    nodes_result_map[mr.node_name][key] = [mr]
            else:
                nodes_result_map[mr.node_name] = {
                    key: [mr]
                }

        results = []
        for node, node_metrics in nodes_result_map.items():
            for metric, values in node_metrics.items():
                vals = []
                for v in values:
                    vals.append(v.value)

                if vals:
                    mv = values[0]
                    mean = sum(vals) / len(vals)
                    results.append(AggregateAgentMetricResult(name=mv.name,
                                                              method=mv.method,
                                                              provider=mv.provider,
                                                              node_name=mv.node_name,
                                                              applies_to=mv.applies_to,
                                                              group=mv.group,
                                                              value=mean,
                                                              min=min(vals),
                                                              max=max(vals),
                                                              count=len(vals),
                                                              individual_results=values if include_individual_results else []).model_dump(mode="json", exclude_unset=True, exclude_none=True))

        return results

    def to_json(self, metric_name: Optional[str] = None, node_name: Optional[str] = None, conversation_id: Optional[str] = None, interaction_id: Optional[str] = None, **kwargs) -> dict:
        """
        Get the agentic metrics results as json

        Args:
            metric_name (Optional[str], optional): Name of metric used to filter the metric results. Defaults to None.
            node_name (Optional[str], optional): Name of the node used to filter the metric results. Defaults to None.
            conversation_id (Optional[str], optional): The conversation id used to filter the metric results. Defaults to None.
            interaction_id (Optional[str], optional): The interaction id used to filter the metric results. Defaults to None.

        Returns:
            dict: The metrics result
        """
        if kwargs.get("exclude_unset") is None:
            kwargs["exclude_unset"] = True

        # If the filters are not specified return the metrics results as it is
        if not (metric_name or node_name or conversation_id or interaction_id):
            return self.model_dump(mode="json", **kwargs)

        # Filter the metric results
        metric_results = [
            r for r in self.metrics_result
            if (node_name is None or r.node_name == node_name)
            and (metric_name is None or r.name == metric_name)
            and (conversation_id is None or r.conversation_id == conversation_id)
            and (interaction_id is None or r.interaction_id == interaction_id)
        ]

        return {"metrics_result": [r.model_dump(mode="json", **kwargs) for r in metric_results]}

    def to_df(self, input_data: Optional[pd.DataFrame] = None,
              interaction_id_field: str = "interaction_id",  wide_format: bool = True) -> pd.DataFrame:
        """
        Get metrics dataframe.

        If the input dataframe is provided, it will be merged with the metrics dataframe.

        Args:
            input_data (Optional[pd.DataFrame], optional): Input data to merge with metrics dataframe.. Defaults to None.
            interaction_id_field (str, optional): Field to use for merging input data and metrics dataframe.. Defaults to "interaction_id".
            wide_format (bool): Determines whether to display the results in a pivot table format. Defaults to True

        Returns:
            pd.DataFrame: Metrics dataframe.
        """

        def converter(m): return m.model_dump(
            exclude={"provider"}, exclude_none=True)

        metrics_df = pd.DataFrame(list(map(converter, self.metrics_result)))
        if input_data is not None:
            metrics_df = input_data.merge(metrics_df, on=interaction_id_field)

        # Return the metric result dataframe
        # if the wide_format is False
        if not wide_format:
            return metrics_df

        # Prepare the dataframe for pivot table view
        def col_name(row):
            if row["applies_to"] == "node":
                return f"{row['node_name']}.{row['name']}"
            if row["applies_to"] == "interaction":
                return f"interaction.{row['name']}"
            # TODO support other types

        metrics_df["idx"] = metrics_df.apply(col_name, axis=1)

        # Pivot the table
        metrics_df_wide = metrics_df.pivot_table(
            index="interaction_id",
            columns="idx",
            values="value"
        ).reset_index().rename_axis("", axis=1)

        # if input_data is provided add
        # it to the pivot table
        if input_data is not None:
            metrics_df_wide = input_data.merge(
                metrics_df_wide, on=interaction_id_field)
        return metrics_df_wide
