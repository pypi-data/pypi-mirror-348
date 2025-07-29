# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------

import os
from typing import Annotated, Optional

from pydantic import BaseModel, Field, model_validator
from typing_extensions import Self

from ibm_watsonx_gov.config.gen_ai_configuration import GenAIConfiguration
from ibm_watsonx_gov.entities.enums import EvaluatorFields


class TracingConfiguration(BaseModel):
    """
    The tracing configuration details.
    One of project_id or space_id is required.
    """
    tracing_url: Annotated[str | None, Field(title="Tracing Url",
                                             description="The tracing url.",
                                             default=None)]  # TODO set a valid default value
    project_id: Annotated[str | None, Field(title="Project ID",
                                            description="The project id.",
                                            default=None)]
    space_id: Annotated[str | None, Field(title="Space ID",
                                          description="The space id.",
                                          default=None)]

    @model_validator(mode="after")
    def validate_fields(self) -> Self:
        if not (self.project_id or self.space_id):
            raise ValueError(
                "The project or space id is required. Please provide one of them and retry.")

        return self

    @classmethod
    def create_from_env(cls):
        # TODO get the default value and validate the tracing url env variable
        tracing_url = os.getenv("WATSONX_TRACING_URL") or ""
        project_id = os.getenv("PROJECT_ID")
        space_id = os.getenv("SPACE_ID")

        return TracingConfiguration(
            tracing_url=tracing_url,
            project_id=project_id,
            space_id=space_id
        )


class AgenticAIConfiguration(GenAIConfiguration):
    """
    The configuration interface for Agentic AI tools and applications.
    """
    input_fields: Annotated[Optional[list[str]], Field(title="Input Fields",
                                                       description="The list of model input fields in the data.",
                                                       default=[],
                                                       examples=[["question", "context1", "context2"]])]

    interaction_id_field: Annotated[Optional[str], Field(title="Interaction id field",
                                                         description="The interaction identifier field name.",
                                                         examples=[
                                                             "interaction_id"],
                                                         default="interaction_id")]

    conversation_id_field: Annotated[Optional[str], Field(title="Conversation id field",
                                                          description="The conversation identifier field name.",
                                                          examples=[
                                                              "conversation_id"],
                                                          default="conversation_id")]

    @model_validator(mode="after")
    def validate_fields(self) -> Self:
        return self

    @classmethod
    def create_configuration(cls, *, app_config: Optional[Self],
                             method_config: Optional[Self],
                             defaults: list[EvaluatorFields],
                             add_record_fields: bool = True) -> Self:
        """
        Creates a configuration object based on the provided parameters.

        Args:
            app_config (Optional[Self]): The application configuration.
            method_config (Optional[Self]): The method configuration.
            defaults (list[EvaluatorFields]): The default fields to include in the configuration.
            add_record_fields (bool, optional): Whether to add record fields to the configuration. Defaults to True.

        Returns:
            Self: The created configuration object.
        """

        if method_config is not None:
            return method_config

        if app_config is not None:
            return app_config

        mapping = EvaluatorFields.get_default_fields_mapping()
        config = {field.value: mapping[field] for field in defaults}

        if not add_record_fields:
            return cls(**config)

        system_fields = [EvaluatorFields.RECORD_ID_FIELD,
                         EvaluatorFields.RECORD_TIMESTAMP_FIELD,
                         EvaluatorFields.INTERACTION_ID_FIELD,
                         EvaluatorFields.CONVERSATION_ID_FIELD]
        for field in system_fields:
            if field not in defaults:
                config[field.value] = EvaluatorFields.get_default_fields_mapping()[
                    field]
        return cls(**config)
