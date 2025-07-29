# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------

import json
from collections import defaultdict
from pathlib import Path
from typing import Annotated, Dict, Generator, List, Union

from pydantic import Field, TypeAdapter

from ibm_watsonx_gov.config.agentic_ai_configuration import \
    AgenticAIConfiguration
from ibm_watsonx_gov.entities.enums import MetricGroup
from ibm_watsonx_gov.entities.evaluation_result import AgentMetricResult
from ibm_watsonx_gov.entities.metric import GenAIMetric
from ibm_watsonx_gov.evaluate.impl.evaluate_metrics_impl import \
    _evaluate_metrics
from ibm_watsonx_gov.traces.span_tree import SpanNode, SpanTree
from ibm_watsonx_gov.utils.python_utils import get

METRICS_UNION = Annotated[Union[tuple(GenAIMetric.__subclasses__())], Field(
    discriminator="name")]

TARGETED_TRACE_NAMES = [
    "openai.embeddings",
    "openai.chat",
    # TODO: check attributes for other frameworks as well.
    # Add additional names if more black box metrics need to be calculated
]
ONE_M = 1000000
COST_METADATA = {  # Costs per 1M tokens
    "openai": {
        "gpt-4o": {"input": 5.0, "output": 15.0},
        "gpt-4-turbo": {"input": 10.0, "output": 30.0},
        "gpt-4": {"input": 30.0, "output": 60.0},
        "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
        # Note: Added from web
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "text-embedding-3-small": {"input": 0.02, "output": 0.0},
    },
    "anthropic": {
        "claude-3-opus": {"input": 15.0, "output": 75.0},
        "claude-3-sonnet": {"input": 3.0, "output": 15.0},
        "claude-3-haiku": {"input": 0.25, "output": 1.25},
    },
    "google": {
        "gemini-1.5-pro": {"input": 7.0, "output": 21.0},
        "gemini-1.5-flash": {"input": 0.35, "output": 1.05},
    },
    "mistral": {
        "mistral-large": {"input": 8.0, "output": 24.0},
        "mistral-7b": {"input": 0.25, "output": 0.80},
        "mixtral-8x7b": {"input": 1.00, "output": 3.00},
    },
    "cohere": {
        "command-r": {"input": 1.00, "output": 3.00},
    },
    "ai21": {
        "jurassic-2": {"input": 10.0, "output": 20.0},
    },
}


class TraceUtils:

    @classmethod
    def build_trees(cls, spans: List) -> Dict[str, SpanTree]:
        """
        Converts the given list of spans for traces into the Span Trees.
        :spans: The list of spans.

        :returns: The dictionary of SpanTrees against respective trace IDs.
        """
        span_trees = dict()

        # Maintaining list of orphan spans whose parents are not yet added to the tree
        orphan_spans = dict()
        for log in spans:
            for resource_span in log.get("resource_spans", list()):
                service_name = None
                resource_attributes = get(resource_span, "resource.attributes")
                for resource_attribute in resource_attributes:
                    att_key = get(resource_attribute, "key")
                    if att_key == "service.name":
                        service_name = get(
                            resource_attribute, "value.string_value")
                for scope_span in get(resource_span, "scope_spans", list()):
                    for span in get(scope_span, "spans", list()):
                        trace_id = get(span, "trace_id")
                        parent_span_id = get(span, "parent_span_id")
                        if parent_span_id is None:
                            # Root/First span for the trace is found
                            root_span = SpanNode(
                                service_name=service_name,
                                span=span
                            )
                            # Initializing the tree
                            span_tree = SpanTree(root_span)
                            span_trees[trace_id] = span_tree
                        else:
                            span_node = SpanNode(
                                service_name=service_name,
                                span=span
                            )
                            span_tree = get(span_trees, trace_id)
                            if span_tree is None:
                                # Tree hasn't been formed yet
                                if trace_id not in orphan_spans:
                                    orphan_spans[trace_id] = [span_node]
                                else:
                                    orphan_spans[trace_id].append(span_node)
                            else:
                                inserted = span_tree.insert(span_node)
                                if not inserted:
                                    # Parent not yet added to the tree
                                    if trace_id not in orphan_spans:
                                        orphan_spans[trace_id] = [span_node]
                                    else:
                                        orphan_spans[trace_id].append(
                                            span_node)

        for trace_id in orphan_spans:
            trace_orphan_spans = get(orphan_spans, trace_id)
            span_tree = get(span_trees, trace_id)
            if span_tree is None:
                # Root span was not present, skipping this
                continue

            while len(trace_orphan_spans) > 0:
                inserted_spans = []
                for orphan_span in trace_orphan_spans:
                    # Inserting the orphan span
                    inserted = span_tree.insert(orphan_span)
                    if inserted:
                        inserted_spans.append(orphan_span)

                # Removing inserted spans from orphan list for next iteration
                for ins_span in inserted_spans:
                    trace_orphan_spans.remove(ins_span)

                if len(inserted_spans) == 0:
                    # No parents were found for any orphan spans
                    break

        return span_trees

    @staticmethod
    def convert_array_value(array_obj: Dict) -> List:
        """Convert OTEL array value to Python list"""
        return [
            item.get("string_value")
            or int(item.get("int_value", ""))
            or float(item.get("double_value", ""))
            or bool(item.get("bool_value", ""))
            for item in array_obj.get("values", [])
        ]

    @staticmethod
    def stream_trace_data(file_path: Path) -> Generator:
        """Generator that yields spans one at a time."""
        with open(file_path) as f:
            for line in f:
                try:
                    yield json.loads(line)
                except json.JSONDecodeError as e:
                    print(f"Failed to parse line: {line}\nError: {e}")

    @staticmethod
    def __prase_and_extract_meta_data(span_tree: SpanTree, meta_data: dict) -> None:
        """
        Extract meta data required to calculate agent level metrics from spans
        """
        for child in span_tree.children:
            TraceUtils.__prase_and_extract_meta_data(child, meta_data)
        span = span_tree.node.span
        if span.get("name") in TARGETED_TRACE_NAMES:
            attributes = {}
            for attr in span.get("attributes"):
                key = attr["key"]
                value_obj = attr.get("value", {})
                # Handle each value type
                if "string_value" in value_obj:
                    attributes[key] = value_obj["string_value"]
                elif "bool_value" in value_obj:
                    attributes[key] = bool(value_obj["bool_value"])
                elif "int_value" in value_obj:
                    attributes[key] = int(value_obj["int_value"])
                elif "double_value" in value_obj:
                    attributes[key] = float(value_obj["double_value"])
                elif "array_value" in value_obj:
                    attributes[key] = TraceUtils.convert_array_value(
                        value_obj["array_value"]
                    )
                else:
                    attributes[key] = None

            provider = attributes.get("gen_ai.system")
            llm_type = attributes.get("llm.request.type")
            model = attributes.get("gen_ai.request.model")

            if not llm_type or not model:
                return

            cost_key = (provider, llm_type, model)
            meta_data["cost"][span.get("trace_id")].append(
                {
                    "provider_details": cost_key,
                    "total_prompt_tokens": attributes.get("gen_ai.usage.prompt_tokens", 0),
                    "total_completion_tokens": attributes.get(
                        "gen_ai.usage.completion_tokens", 0
                    ),
                    "total_tokens": attributes.get("llm.usage.total_tokens", 0),
                }
            )

    @staticmethod
    def calculate_cost(usage_data: List[dict]) -> float:
        """Calculate cost for given list of usage."""
        total_cost = 0.0

        for data in usage_data:
            (provider, _, model) = data["provider_details"]
            provider = provider.lower()
            model = model.lower()

            try:
                model_pricing = COST_METADATA[provider][model]
            except KeyError:
                raise ValueError(
                    f"Pricing not available for {provider}/{model}")

            # Calculate costs (per 1M tokens)
            input_cost = (data["total_prompt_tokens"] /
                          ONE_M) * model_pricing["input"]
            output_cost = (data["total_completion_tokens"] / ONE_M) * model_pricing[
                "output"
            ]
            total_cost += input_cost + output_cost

        return total_cost

    @staticmethod
    def compute_metrics_from_traces(spans: list[dict], api_client) -> list[AgentMetricResult]:
        span_tree = TraceUtils.build_trees(spans)

        results = []
        for k, v in span_tree.items():
            # Interaction level metrics
            span = v.node.span
            interaction_id = span.get("trace_id")
            results.append(AgentMetricResult(name="latency",
                                             value=(int(
                                                 span.get("end_time_unix_nano")) - int(span.get("start_time_unix_nano")))/1000000000,
                                             group=MetricGroup.PERFORMANCE,
                                             applies_to="interaction",
                                             interaction_id=interaction_id))

            # Node level metrics
            for c in v.children:
                span = c.node.span
                node_name, metrics_configuration, data = None, None, None
                for attr in span.get("attributes"):
                    if attr.get("key") == "traceloop.entity.name":
                        node_name = attr.get("value").get("string_value")
                    if attr.get("key") == "wxgov.metrics_configuration":
                        metrics_configuration = json.loads(
                            attr.get("value").get("string_value"))
                    if attr.get("key") == "traceloop.entity.input":
                        inputs = json.loads(
                            attr.get("value").get("string_value")).get("inputs")
                        if data:
                            data.update(inputs)
                        else:
                            data = inputs
                    if attr.get("key") == "traceloop.entity.output":
                        outputs = json.loads(
                            attr.get("value").get("string_value")).get("outputs")
                        if data:
                            data.update(outputs)
                        else:
                            data = outputs

                if node_name == "__start__":
                    continue

                if not metrics_configuration:
                    metrics_configuration = TraceUtils.search_attribute(
                        spans=c.children, attribute_name="wxgov.metrics_configuration")

                if metrics_configuration:
                    config = AgenticAIConfiguration(
                        **metrics_configuration.get("configuration"))
                    metrics = [TypeAdapter(
                        METRICS_UNION).validate_python(m) for m in metrics_configuration.get("metrics")]
                    metric_result = _evaluate_metrics(configuration=config, data=data,
                                                      metrics=metrics, api_client=api_client).to_dict()
                    for mr in metric_result:
                        node_result = {
                            "applies_to": "node",
                            "interaction_id": interaction_id,
                            "node_name": node_name,
                            **mr
                        }

                        results.append(AgentMetricResult(**node_result))

                # Add latency metric result
                results.append(AgentMetricResult(name="latency",
                                                 value=(int(
                                                     span.get("end_time_unix_nano")) - int(span.get("start_time_unix_nano")))/1e9,
                                                 group=MetricGroup.PERFORMANCE,
                                                 applies_to="node",
                                                 interaction_id=interaction_id,
                                                 node_name=node_name))

                results.extend(TraceUtils.__get_results_from_events(
                    span.get("events"), interaction_id, node_name))

                # print(span)

        results.extend(
            TraceUtils.__extract_interaction_cost_latency_metrics_from_spans(span_tree))
        return results

    @staticmethod
    def search_attribute(spans, attribute_name):
        attr_value = None
        if not spans:
            return attr_value

        for sp in spans:
            sp_node = sp.node.span
            for attr in sp_node.get("attributes"):
                if attr.get("key") == attribute_name:
                    attr_value = json.loads(
                        attr.get("value").get("string_value"))
            if not attr_value:
                attr_value = TraceUtils.search_attribute(
                    sp.children, attribute_name)
        return attr_value

    @staticmethod
    def __get_results_from_events(events, interaction_id, node_name):
        results = []
        if not events:
            return results

        for event in events:
            for attr in event.get("attributes"):
                if attr.get("key") == "attr_wxgov.metric_result":
                    mr = json.loads(
                        attr.get("value").get("string_value"))
                    mr.update({
                        "node_name": node_name,
                        "interaction_id": interaction_id
                    })
                    results.append(AgentMetricResult(**mr))

        return results

    @staticmethod
    def __extract_interaction_cost_latency_metrics_from_spans(span_trees: dict) -> list:
        """
        Parse each spans and extract agent level metrics from it
        If parent span of current span_tree is not associated with any of interaction, skip the process
        """
        metrics_result = []
        meta_data = defaultdict(lambda: defaultdict(list))
        for trace_id, span_tree in span_trees.items():
            skip = True
            for attribute in span_tree.node.span.get("attributes"):
                if attribute["key"] == "traceloop.entity.output":
                    skip = False
                    continue
            if skip:
                # Skip processing of unwanted span trees.
                continue
            TraceUtils.__prase_and_extract_meta_data(span_tree, meta_data)

        for metric, data in meta_data.items():
            for trace_id, i_data in data.items():
                if metric == "cost":
                    metric_value = TraceUtils.calculate_cost(i_data)
                agent_mr = {
                    "name": metric,
                    "value": metric_value,
                    "interaction_id": trace_id,
                    "applies_to": "interaction",
                }

                metrics_result.append(AgentMetricResult(**agent_mr))

        return metrics_result
