# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------
import json
import pandas as pd
from ibm_watsonx_gov.config import GenAIConfiguration
from ibm_watsonx_gov.clients.usage_client import validate_usage_client
import requests
from ibm_watsonx_gov.entities.evaluation_result import (AggregateMetricResult,
                                                        RecordMetricResult)
from ibm_watsonx_gov.entities.enums import EvaluationProvider
from ibm_watsonx_gov.entities.enums import MetricGroup
from ibm_watsonx_gov.entities.base_classes import Error
from concurrent.futures import ThreadPoolExecutor


class DetectorsProvider():

    def __init__(
        self,
        configuration: GenAIConfiguration,
        metric_name: str,
        metric_method: str,
        metric_group: MetricGroup = None,
        **kwargs,
    ) -> None:
        service_url = self.get_service_url(kwargs.get("api_client"))
        self.base_url = "{}/v2/text_detections".format(service_url)
        self.configuration: GenAIConfiguration = configuration
        self.configuration_: dict[str, any] = {}
        self.metric_name = metric_name
        self.metric_method = metric_method
        self.metric_group = metric_group
        validate_usage_client(kwargs.get("usage_client"))

    def evaluate(self, data: pd.DataFrame) -> AggregateMetricResult:
        """
        Entry point method to compute the configured detectors-based metrics.
        Args:
            data: Input test data
        """
        try:
            json_payloads, record_ids = self.__pre_process_data(data=data)
            result = self.__compute_metric(json_payloads)
            aggregated_result = self.__post_process(result, record_ids)
            return aggregated_result

        except Exception as e:
            raise Exception(
                f"Error while computing metrics: {self.metric_name}. Reason: {str(e)}")

    def __pre_process_data(self, data: pd.DataFrame):
        """
        Creates payload for each row in the test data.
        """
        input_content = data[self.configuration.input_fields[0]].to_list()
        payloads_json = self.__get_json_payloads(input_content)
        record_ids = data[self.configuration.record_id_field].to_list()
        return payloads_json, record_ids

    def __compute_metric(self, api_payloads: list):
        """
        Calls the detections API and returns the response.
        """
        responses = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            responses = list(executor.map(self.send_request, api_payloads))
        return responses

    def __post_process(self, results: list, record_ids: list) -> AggregateMetricResult:
        """
        Process the responses and aggregate the results.
        """
        record_level_metrics: list[RecordMetricResult] = []
        values = []
        errors = []
        for result, record_id in zip(results, record_ids):
            record_data = {
                "name": self.metric_name,
                "method": self.metric_method,
                "provider": EvaluationProvider.DETECTORS.value,
                "group": self.metric_group,
                "record_id": record_id
            }

            if "error" in result:
                error_msg = result["error"].message_en

                record_level_metrics.append(RecordMetricResult(
                    **record_data,
                    value=error_msg
                ))
                errors.append(result["error"])
            else:
                value = result["detections"][0]["value"]
                record_level_metrics.append(RecordMetricResult(
                    **record_data,
                    value=value
                ))
                values.append(value)


        # creating AggregateMetricResult
        if values:
            mean_val = round(sum(values) / len(values), 4)
            min_val = min(values)
            max_val = max(values)
            value = mean_val
            error_info = {}
        else:
            mean_val = min_val = max_val = None
            value = "Error"
            error_info = {"errors": errors}

        aggregated_result = AggregateMetricResult(
            name=self.metric_name,
            method=self.metric_method,
            group=self.metric_group,
            provider=EvaluationProvider.DETECTORS.value,
            value=value,
            total_records=len(results),
            record_level_metrics=record_level_metrics,
            min=min_val,
            max=max_val,
            mean=mean_val,
            **error_info
        )

        # return the aggregated result
        return aggregated_result

    def __get_json_payloads(self, contents: list) -> list:
        # Method to create the request payload.
        json_payloads = []
        for content in contents:
            payload_json = {
                "detectors": {
                    self.metric_name: {}
                },
                "input": {
                    "content": content
                }
            }
            json_payloads.append(json.dumps(payload_json))
        return json_payloads

    def __get_headers(self):
        # Method to create request headers
        headers = {}
        headers["Content-Type"] = "application/json"
        headers["Authorization"] = f"Bearer {self.wos_client.authenticator.token_manager.get_token()}"
        return headers

    def send_request(self, api_payload):
        response = requests.post(
            url=self.base_url, headers=self.__get_headers(), data=api_payload)
        response_status = response.status_code
        if response_status != 200:
            response = response.text if not isinstance(response, str) else response
            return {"error": Error(code=str(response_status),
                         message_en=str(json.loads(str(response))))}
        else:
            return json.loads(response.text)

    def get_service_url(self, api_client):
        """
        Sets the wos_client and returns the service url
        """
        api_client = api_client
        self.wos_client = api_client.wos_client
        return self.wos_client.service_url