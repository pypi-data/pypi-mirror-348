# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------

from typing import Annotated, Callable, Dict, Optional, Union

from pydantic import Field, model_validator
from typing_extensions import Self

from ibm_watsonx_gov.entities.base_classes import BaseConfiguration
from ibm_watsonx_gov.entities.enums import TaskType
from ibm_watsonx_gov.entities.llm_judge import LLMJudge
from ibm_watsonx_gov.entities.metric import Locale


class GenAIConfiguration(BaseConfiguration):
    task_type: Annotated[TaskType | None, Field(title="Task Type",
                                                description="The generative task type.",
                                                default=None,
                                                examples=[TaskType.RAG])]
    input_fields: Annotated[list[str], Field(title="Input Fields",
                                             description="The list of model input fields in the data.",
                                             examples=[["question", "context1", "context2"]])]
    question_field: Annotated[str | None, Field(title="Question Field",
                                                description="The question field in the input fields.",
                                                default=None,
                                                examples=["question"])]
    context_fields: Annotated[list[str], Field(title="Context Fields",
                                               description="The list of context fields in the input fields.",
                                               default=[],
                                               examples=[["context1", "context2"]])]
    output_fields: Annotated[list[str], Field(title="Output Fields",
                                              description="The list of model output fields in the data.",
                                              default=[],
                                              examples=[["output"]])]
    reference_fields: Annotated[list[str], Field(title="Reference Fields",
                                                 description="The list of reference fields in the data.",
                                                 default=[],
                                                 examples=[["reference"]])]
    locale: Annotated[Locale | None, Field(title="Locale",
                                           description="The language locale of the input, output and reference fields in the data.",
                                           default=None)]
    tools: Annotated[Union[list[Callable], list[Dict]], Field(title="Tools",
                                                              description="The list of tools used by the LLM.",
                                                              default=[],
                                                              examples=[
                                                                  ["function1",
                                                                   "function2"]
                                                              ])]
    tool_calls_field: Annotated[Optional[str] | None, Field(title="Tool Calls Field",
                                                            description="The tool calls field in the input fields.",
                                                            default=None,
                                                            examples=["tools_used"])]

    llm_judge: Annotated[LLMJudge | None, Field(title="LLM Judge",
                                                description="LLM as Judge Model details.",
                                                default=None)]

    @model_validator(mode="after")
    def validate_fields(self) -> Self:

        if self.task_type == TaskType.RAG:
            if not self.question_field or not self.context_fields:
                raise ValueError(
                    "question_field and context_fields are required for RAG task type.")

        if self.question_field:
            if self.question_field not in self.input_fields:
                raise ValueError(
                    f"The question field {self.question_field} is not present in input fields {self.input_fields}.")

            if self.question_field in self.context_fields:
                raise ValueError(
                    f"The question field {self.question_field} should not be provided in the context fields {self.context_fields}.")

        if self.context_fields and not all(column in self.input_fields for column in self.context_fields):
            raise ValueError(
                f"The context fields {self.context_fields} are not present in input fields {self.input_fields}.")

        return self
