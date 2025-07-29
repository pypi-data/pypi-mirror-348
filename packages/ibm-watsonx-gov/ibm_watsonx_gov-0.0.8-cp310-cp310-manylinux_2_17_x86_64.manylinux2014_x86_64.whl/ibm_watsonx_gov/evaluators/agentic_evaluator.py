# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------

import os
from copy import deepcopy
from pathlib import Path
from threading import Lock
from typing import Annotated, Callable, List, Optional, Set
from uuid import uuid4

from pydantic import Field, PrivateAttr

from ibm_watsonx_gov.ai_experiments.ai_experiments_client import \
    AIExperimentsClient
from ibm_watsonx_gov.config import AgenticAIConfiguration
from ibm_watsonx_gov.config.agentic_ai_configuration import \
    TracingConfiguration
from ibm_watsonx_gov.entities import ai_experiment as ai_experiment_entity
from ibm_watsonx_gov.entities.ai_evaluation import AIEvaluationAsset
from ibm_watsonx_gov.entities.ai_experiment import (AIExperiment,
                                                    AIExperimentRun)
from ibm_watsonx_gov.entities.evaluation_result import (
    AgenticEvaluationResult, AgentMetricResult)
from ibm_watsonx_gov.entities.metric import GenAIMetric
from ibm_watsonx_gov.entities.node import Node
from ibm_watsonx_gov.evaluate.impl.evaluate_metrics_impl import \
    _evaluate_metrics
from ibm_watsonx_gov.evaluators.base_evaluator import BaseEvaluator
from ibm_watsonx_gov.metrics import (AnswerSimilarityMetric,
                                     ContextRelevanceMetric,
                                     FaithfulnessMetric)
from ibm_watsonx_gov.metrics.answer_similarity.answer_similarity_decorator import \
    AnswerSimilarityDecorator
from ibm_watsonx_gov.metrics.context_relevance.context_relevance_decorator import \
    ContextRelevanceDecorator
from ibm_watsonx_gov.metrics.faithfulness.faithfulness_decorator import \
    FaithfulnessDecorator
from ibm_watsonx_gov.traces.span_exporter import WxGovSpanExporter
from ibm_watsonx_gov.traces.trace_utils import TraceUtils
from ibm_watsonx_gov.utils.python_utils import add_if_unique
from ibm_watsonx_gov.utils.singleton_meta import SingletonMeta

PROCESS_TRACES = True


try:
    from agent_analytics.instrumentation import agent_analytics_sdk
except ImportError:
    PROCESS_TRACES = False


update_lock = Lock()
TRACE_LOG_FILE_NAME = os.getenv("TRACE_LOG_FILE_NAME", "experiment_traces")
TRACE_LOG_FILE_PATH = os.getenv("TRACE_LOG_FILE_PATH", "./wxgov_traces")


class AgenticEvaluator(BaseEvaluator, metaclass=SingletonMeta):
    """
    The class to evaluate agentic application.

    Examples:
        1. Basic usage with experiment tracking
            .. code-block:: python

                agentic_evaluator = AgenticEvaluator(tracing_configuration=TracingConfiguration(project_id=project_id))
                agentic_evaluator.track_experiment(name="my_experiment")
                agentic_evaluator.start_run(name="run1")
                # Invoke the agentic application
                agentic_evaluator.end_run()
                result = agentic_evaluator.get_result()

        2. Basic usage without experiment tracking
            .. code-block:: python

                agentic_evaluator = AgenticEvaluator()
                agentic_evaluator.start_run()
                # Invoke the agentic application
                agentic_evaluator.end_run()
                result = agentic_evaluator.get_result()
    """
    agentic_ai_configuration: Annotated[Optional[AgenticAIConfiguration],
                                        Field(name="Configuration object", default=None)]
    tracing_configuration: Annotated[Optional[TracingConfiguration], Field(title="Tracing Configuration",
                                                                           description="Tracing Configuration",
                                                                           default=None)]
    ai_experiment_client:  Annotated[Optional[AIExperimentsClient],
                                     Field(name="AI experiments client", default=None)]
    __latest_experiment_name: Annotated[Optional[str], PrivateAttr(
        default=None)]
    __latest_experiment_id: Annotated[Optional[str], PrivateAttr(
        default=None)]
    __experiment_results: Annotated[dict,
                                    PrivateAttr(default={})]
    __run_results: Annotated[dict[str, list[AgentMetricResult]],
                             PrivateAttr(default={})]
    __metric_results: Annotated[list[AgentMetricResult],
                                PrivateAttr(default=[])]
    """__metric_results holds the results of all the evaluations done for a particular evaluation instance."""
    __execution_counts: Annotated[dict[str, dict[str, int]],
                                  PrivateAttr(default={})]
    """__execution_counts holds the execution count for a particular node, for a given record_id."""
    __nodes_being_run: Annotated[dict[str, Set[str]],
                                 PrivateAttr(default={})]
    """__nodes_being_run holds the name of the current nodes being run for a given record_id. Multiple decorators can be applied on a single node using chaining. We don't want to hold multiple copies of same node here."""
    __latest_run_name: Annotated[str, PrivateAttr(default=None)]
    __nodes: Annotated[list[Node], PrivateAttr(default=[])]
    __experiment_run_details: Annotated[AIExperimentRun, PrivateAttr(
        default=None)]

    def __init__(self, /, **data):
        """
        Initialize the AgenticEvaluator object and start the tracing framework.
        """
        super().__init__(**data)
        # Initialize the agent analytics sdk
        if PROCESS_TRACES:
            tracing_url = None
            tracing_config = data.get("tracing_configuration")
            if tracing_config:
                tracing_url = tracing_config.tracing_url

            agent_analytics_sdk.initialize_logging(
                tracer_type=agent_analytics_sdk.SUPPORTED_TRACER_TYPES.CUSTOM,
                custom_exporter=WxGovSpanExporter(
                    file_name=TRACE_LOG_FILE_NAME,
                    storage_path=TRACE_LOG_FILE_PATH,
                    service_endpoint=tracing_url
                ),
            )
        self.__latest_experiment_name = "experiment_1"

    def track_experiment(self, name: str = "experiment_1", description: str = None, use_existing: bool = True) -> str:
        """
        Start tracking an experiment for the metrics evaluation. 
        The experiment will be created if it doesn't exist. 
        If an existing experiment with the same name is found, it will be reused based on the flag use_existing. 

        Args:
            project_id (string): The project id to store the experiment.
            name (string): The name of the experiment.
            description (str): The description of the experiment.
            use_existing (bool): The flag to specify if the experiment should be reused if an existing experiment with the given name is found.

        Returns:
            The ID of AI experiment asset
        """
        self.__latest_experiment_name = name
        # Checking if the ai_experiment_name already exists with given name if use_existing is enabled.
        # If it does reuse it, otherwise creating a new ai_experiment
        # Set the experiment_name and experiment_id
        self.ai_experiment_client = AIExperimentsClient(
            api_client=self.api_client,
            project_id=self.tracing_configuration.project_id
        )
        ai_experiment = None
        if use_existing:
            ai_experiment = self.ai_experiment_client.search(name)

        # If no AI experiment exists with specified name or use_existing is False, create new AI experiment
        if not ai_experiment:
            ai_experiment_details = AIExperiment(
                name=name,
                description=description or "AI experiment for Agent governance"
            )
            ai_experiment = self.ai_experiment_client.create(
                ai_experiment_details)

        ai_experiment_id = ai_experiment.asset_id

        # Experiment id will be set when the experiment is tracked and not set when the experiment is not tracked
        self.__latest_experiment_id = ai_experiment_id
        self.__run_results = {}
        return ai_experiment_id

    def start_run(self, name: str = "run_1") -> AIExperimentRun:
        """
        Start a run to track the metrics computation within an experiment.
        This method is required to be called before any metrics computation.

        Args:
            name (string): The evaluation run name

        Returns:
            The details of experiment run like id, name, description etc.
        """
        self.__latest_run_name = name
        self.__experiment_results[self.__latest_experiment_name] = self.__run_results
        self.__run_results[self.__latest_run_name] = self.__metric_results
        # Having experiment id indicates user is tracking experiments
        if self.__latest_experiment_id:
            # Create run object, having experiment id indicates user is tracking experiments
            self.__experiment_run_details = AIExperimentRun(
                run_id=str(uuid4()),
                run_name=name
            )

        return self.__experiment_run_details

    def end_run(self):
        """
        End a run to collect and compute the metrics within the current run.
        """
        self.__compute_metrics_from_traces()
        self.__set_nodes()
        self.__run_results[self.__latest_run_name] = deepcopy(
            self.__metric_results)
        # Having experiment id indicates user is tracking experiments and its needed to submit the run details
        if self.__latest_experiment_id:
            self.__store_run_results()

        self.__reset_results()

    def compare_ai_experiments(self,
                               ai_experiments: List[AIExperiment] = None,
                               ai_evaluation_details: AIEvaluationAsset = None
                               ) -> str:
        """
        Creates an AI Evaluation asset to compare AI experiment runs.

        Args:
            ai_experiments (List[AIExperiment], optional):
                List of AI experiments to be compared. If all runs for an experiment need to be compared, then specify the runs value as empty list for the experiment.
            ai_evaluation_details (AIEvaluationAsset, optional):
                An instance of AIEvaluationAsset having details (name, description and metrics configuration)
        Returns:
            An instance of AIEvaluationAsset.

        Examples:
            1. Create AI evaluation with list of experiment IDs
            .. code-block:: python

                # Initialize the API client with credentials
                api_client = APIClient(credentials=Credentials(api_key="", url="wos_url"))

                # Create the instance of Agentic evaluator
                evaluator = AgenticEvaluator(api_client=api_client, tracing_configuration=TracingConfiguration(project_id=project_id))

                # [Optional] Define evaluation configuration
                evaluation_config = EvaluationConfig(
                    monitors={
                        "agentic_ai_quality": {
                            "parameters": {
                                "metrics_configuration": {}
                            }
                        }
                    }
                )

                # Create the evaluation asset
                ai_evaluation_details = AIEvaluationAsset(
                    name="AI Evaluation for agent",
                    evaluation_configuration=evaluation_config
                )

                # Compare two or more AI experiments using the evaluation asset
                ai_experiment1 = AIExperiment(
                    asset_id = ai_experiment_id_1,
                    runs = [<Run1 details>, <Run2 details>] # Run details are returned by the start_run method
                )
                ai_experiment2 = AIExperiment(
                    asset_id = ai_experiment_id_2,
                    runs = [] # Empty list means all runs for this experiment will be compared
                )
                ai_evaluation_asset_href = evaluator.compare_ai_experiments(
                    ai_experiments = [ai_experiment_1, ai_experiment_2],
                    ai_evaluation_details=ai_evaluation_asset
                )
        """
        # If experiment runs to be compared are not provided, using all runs from the latest tracked experiment
        if not ai_experiments:
            ai_experiments = [AIExperiment(
                asset_id=self.__latest_experiment_id, runs=[])]

        # Construct experiment_runs map
        ai_experiment_runs = {exp.asset_id: exp.runs for exp in ai_experiments}

        ai_evaluation_asset = self.ai_experiment_client.create_ai_evaluation_asset(
            ai_experiment_runs=ai_experiment_runs,
            ai_evaluation_details=ai_evaluation_details
        )
        ai_evaluation_asset_href = self.ai_experiment_client.get_ai_evaluation_asset_href(
            ai_evaluation_asset)

        return ai_evaluation_asset_href

    def __compute_metrics_from_traces(self):
        """
        Computes the metrics using the traces collected in the log file.
        """
        if PROCESS_TRACES:
            trace_log_file_path = Path(
                f"{TRACE_LOG_FILE_PATH}/{TRACE_LOG_FILE_NAME}.log")
            spans = []
            for span in TraceUtils.stream_trace_data(trace_log_file_path):
                spans.append(span)

            self.__metric_results = TraceUtils.compute_metrics_from_traces(
                spans, self.api_client)

    def __store_run_results(self):
        aggregated_results = self.get_result().get_aggregated_results()

        # Fetchig the nodes details to update in experiment run
        nodes = []
        for node in self.get_nodes():
            nodes.append(ai_experiment_entity.Node(
                id=node.func_name, name=node.name))
        self.__experiment_run_details.nodes = nodes

        # Storing the run result as attachment and update the run info in AI experiment
        self.ai_experiment_client.update(
            self.__latest_experiment_id,
            self.__experiment_run_details,
            aggregated_results
        )

    def __set_nodes(self):
        for result in self.__metric_results:
            if result.applies_to == "node":
                add_if_unique(Node(name=result.node_name, func_name=result.node_name), self.__nodes,
                              ["name", "func_name"])

    def get_nodes(self) -> list[Node]:
        """
        Get the list of nodes used in the agentic application

        Return:
            nodes (list[Node]): The list of nodes used in the agentic application
        """
        return self.__nodes

    def get_result(self, run_name: Optional[str] = None) -> AgenticEvaluationResult:
        """
        Get the AgenticEvaluationResult for the run. By default the result for the latest run is returned.
        Specify the run name to get the result for a specific run.

        Args:
            run_name (string): The evaluation run name

        Return:
            agentic_evaluation_result (AgenticEvaluationResult): The AgenticEvaluationResult object for the run.
        """
        if run_name:
            metric_results = self.__run_results.get(run_name)
        else:
            metric_results = self.__run_results.get(self.__latest_run_name)

        # metric_results = sorted(metric_results)
        return AgenticEvaluationResult(metrics_result=metric_results)

    def __reset_results(self):
        self.__metric_results.clear()
        self.__execution_counts.clear()
        self.__nodes_being_run.clear()
        trace_log_file_path = Path(
            f"{TRACE_LOG_FILE_PATH}/{TRACE_LOG_FILE_NAME}.log")
        with open(trace_log_file_path, "w") as file:
            # Wipe the log file
            pass

    def evaluate_context_relevance(self,
                                   func: Optional[Callable] = None,
                                   *,
                                   configuration: Optional[AgenticAIConfiguration] = None,
                                   metrics: list[GenAIMetric] = [
                                       ContextRelevanceMetric()
                                   ],
                                   compute_online: Optional[bool] = True) -> dict:
        """
        An evaluation decorator for computing context relevance metric on an agentic node.

        For more details, see :class:`ibm_watsonx_gov.metrics.ContextRelevanceMetric`

        Args:
            func (Optional[Callable], optional): The node on which the metric is to be computed.
            configuration (Optional[AgenticAIConfiguration], optional): The configuration specific to this evaluator. Defaults to None.
            metrics (list[GenAIMetric], optional): The list of metrics to compute as part of this evaluator. Defaults to [ ContextRelevanceMetric() ].
            compute_online (Optional[bool], optional): The flag to indicate whether the metric should be computed along with the node execution or not.

        Raises:
            Exception: If there is any error while evaluation.

        Returns:
            dict: The result of the wrapped node.

        Examples:
            1. Basic usage
                .. code-block:: python

                    evaluator = AgenticEvaluator()
                    @evaluator.evaluate_context_relevance
                    def agentic_node(*args, *kwargs):
                        pass

            2. Usage with different thresholds and methods
                .. code-block:: python

                    metric_1 = ContextRelevanceMetric(
                        method="sentence_bert_bge", threshold=MetricThreshold(type="lower_limit", value=0.5))
                    metric_2 = ContextRelevanceMetric(
                        method="sentence_bert_mini_lm", threshold=MetricThreshold(type="lower_limit", value=0.6))

                    evaluator = AgenticEvaluator()
                    @evaluator.evaluate_context_relevance(metrics=[metric_1, metric_2])
                    def agentic_node(*args, *kwargs):
                        pass
        """
        return ContextRelevanceDecorator(api_client=self.api_client,
                                         configuration=self.agentic_ai_configuration,
                                         metric_results=self.__metric_results,
                                         execution_counts=self.__execution_counts,
                                         nodes_being_run=self.__nodes_being_run,
                                         lock=update_lock,
                                         compute_online=compute_online).evaluate_context_relevance(func, configuration=configuration, metrics=metrics)

    def evaluate_answer_similarity(self,
                                   func: Optional[Callable] = None,
                                   *,
                                   configuration: Optional[AgenticAIConfiguration] = None,
                                   metrics: list[GenAIMetric] = [
                                       AnswerSimilarityMetric()
                                   ],
                                   compute_online: Optional[bool] = True) -> dict:
        """
        An evaluation decorator for computing answer similarity metric on an agentic node.

        For more details, see :class:`ibm_watsonx_gov.metrics.AnswerSimilarityMetric`

        Args:
            func (Optional[Callable], optional): The node on which the metric is to be computed.
            configuration (Optional[AgenticAIConfiguration], optional): The configuration specific to this evaluator. Defaults to None.
            metrics (list[GenAIMetric], optional): The list of metrics to compute as part of this evaluator. Defaults to [ AnswerSimilarityMetric() ].
            compute_online (Optional[bool], optional): The flag to indicate whether the metric should be computed along with the node execution or not.

        Raises:
            Exception: If there is any error while evaluation.

        Returns:
            dict: The result of the wrapped node.

        Examples:
            1. Basic usage
                .. code-block:: python

                    evaluator = AgenticEvaluator()
                    @evaluator.evaluate_answer_similarity
                    def agentic_node(*args, *kwargs):
                        pass


            2. Usage with different thresholds and methods
                .. code-block:: python

                    metric_1 = AnswerSimilarityMetric(
                        method="token_k_precision", threshold=MetricThreshold(type="lower_limit", value=0.5))
                    metric_2 = AnswerSimilarityMetric(
                        method="sentence_bert_mini_lm", threshold=MetricThreshold(type="lower_limit", value=0.6))

                    evaluator = AgenticEvaluator()
                    @evaluator.evaluate_answer_similarity(metrics=[metric_1, metric_2])
                    def agentic_node(*args, *kwargs):
                        pass
        """

        return AnswerSimilarityDecorator(api_client=self.api_client,
                                         configuration=self.agentic_ai_configuration,
                                         metric_results=self.__metric_results,
                                         execution_counts=self.__execution_counts,
                                         nodes_being_run=self.__nodes_being_run,
                                         lock=update_lock,
                                         compute_online=compute_online).evaluate_answer_similarity(func, configuration=configuration, metrics=metrics)

    def evaluate_faithfulness(self,
                              func: Optional[Callable] = None,
                              *,
                              configuration: Optional[AgenticAIConfiguration] = None,
                              metrics: list[GenAIMetric] = [
                                  FaithfulnessMetric()
                              ],
                              compute_online: Optional[bool] = True) -> dict:
        """
        An evaluation decorator for computing faithfulness metric on an agentic node.

        For more details, see :class:`ibm_watsonx_gov.metrics.FaithfulnessMetric`

        Args:
            func (Optional[Callable], optional): The node on which the metric is to be computed.
            configuration (Optional[AgenticAIConfiguration], optional): The configuration specific to this evaluator. Defaults to None.
            metrics (list[GenAIMetric], optional): The list of metrics to compute as part of this evaluator. Defaults to [ FaithfulnessMetric() ].
            compute_online (Optional[bool], optional): The flag to indicate whether the metric should be computed along with the node execution or not.

        Raises:
            Exception: If there is any error while evaluation.

        Returns:
            dict: The result of the wrapped node.

        Examples:
            1. Basic usage
                .. code-block:: python

                    evaluator = AgenticEvaluator()
                    @evaluator.evaluate_faithfulness
                    def agentic_node(*args, *kwargs):
                        pass

            2. Usage with different thresholds and methods
                .. code-block:: python

                    metric_1 = FaithfulnessMetric(method="token_k_precision", threshold=MetricThreshold(type="lower_limit", value=0.5))
                    metric_2 = FaithfulnessMetric(method="sentence_bert_mini_lm", threshold=MetricThreshold(type="lower_limit", value=0.6))

                    evaluator = AgenticEvaluator()
                    @evaluator.evaluate_faithfulness(metrics=[metric_1, metric_2])
                    def agentic_node(*args, *kwargs):
                        pass
        """

        return FaithfulnessDecorator(api_client=self.api_client,
                                     configuration=self.agentic_ai_configuration,
                                     metric_results=self.__metric_results,
                                     execution_counts=self.__execution_counts,
                                     nodes_being_run=self.__nodes_being_run,
                                     lock=update_lock,
                                     compute_online=compute_online).evaluate_faithfulness(func, configuration=configuration, metrics=metrics)
