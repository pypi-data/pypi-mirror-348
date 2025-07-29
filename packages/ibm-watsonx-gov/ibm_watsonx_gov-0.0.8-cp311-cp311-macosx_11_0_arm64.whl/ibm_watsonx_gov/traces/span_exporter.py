# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------


import json
import threading
from concurrent.futures import ThreadPoolExecutor

import requests

try:
    from google.protobuf.json_format import MessageToDict
    from opentelemetry.exporter.otlp.proto.common.trace_encoder import \
        encode_spans
    from opentelemetry.proto.trace.v1.trace_pb2 import TracesData
    from opentelemetry.sdk.trace import ReadableSpan
    from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult
except ImportError:
    pass
from pathlib import Path
from typing import Optional, Sequence


class WxGovSpanExporter(SpanExporter):
    def __init__(
        self,
        file_name: str,
        storage_path: str,
        service_endpoint: Optional[str] = None,
        timeout: int = 5,
        max_workers: int = 2,
    ):
        """
        Initialize the exporter with file storage and optional remote forwarding.

        Args:
            file_name: Base name for the trace file (without extension)
            storage_path: Directory to store trace files
            service_endpoint: Optional URL for remote tracing service
            timeout: Timeout in seconds for remote requests
            max_workers: Maximum threads for async operations
        """
        self.storage_path = Path(storage_path)
        self.service_endpoint = service_endpoint
        self.file_path = self.storage_path / f"{file_name}.log"
        self.timeout = timeout
        self._lock = threading.Lock()
        self._executor = ThreadPoolExecutor(max_workers=max_workers)

        # Ensure storage directory exists
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self._initialize_trace_file()

    def _initialize_trace_file(self) -> None:
        """Initialize the trace file with file"""
        with self._lock, self.file_path.open("w") as f:
            pass

    def _serialize_spans(self, spans: Sequence[ReadableSpan]) -> bytes:
        """Serialize spans to protobuf format efficiently"""
        return encode_spans(spans).SerializeToString()

    def _store_locally(self, spans: bytes) -> None:
        """Append spans to the trace file in a thread-safe manner."""
        try:
            traces = TracesData.FromString(spans)
            traces_dict = MessageToDict(
                traces, preserving_proto_field_name=True)
            with self._lock, self.file_path.open("a") as f:
                json.dump(traces_dict, f)
                f.write("\n")
        except Exception as e:
            print(f"Failed to write to trace file: {e}")

    def _forward_to_service(self, serialized_data: bytes) -> None:
        """Forward spans to the centralized tracing service asynchronously"""
        if not self.service_endpoint:
            return

        try:
            response = requests.post(
                self.service_endpoint,
                data=serialized_data,
                headers={"Content-Type": "application/x-protobuf"},
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to forward traces to service: {e}")

    def export(self, spans: Sequence[ReadableSpan]) -> SpanExportResult:
        """Export spans to local file and optionally to remote service."""
        if not spans:
            return SpanExportResult.SUCCESS

        try:
            # Serialize once for both local and remote
            serialized_data = self._serialize_spans(spans)

            self._store_locally(serialized_data)

            # Remote forwarding in background thread if endpoint configured
            if self.service_endpoint:
                self._executor.submit(
                    self._forward_to_service, serialized_data)

            return SpanExportResult.SUCCESS
        except Exception as e:
            print(f"Error exporting spans: {e}")
            return SpanExportResult.FAILURE

    def shutdown(self) -> None:
        """Clean up resources when exporter is no longer needed"""
        self._executor.shutdown(wait=True)
