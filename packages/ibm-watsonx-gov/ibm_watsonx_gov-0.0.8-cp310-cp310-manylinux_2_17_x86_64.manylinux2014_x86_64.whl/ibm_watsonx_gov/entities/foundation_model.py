# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------

from typing import Annotated, Callable

from pydantic import BaseModel, Field

from ibm_watsonx_gov.entities.model_provider import (AzureOpenAIModelProvider,
                                                     CustomModelProvider,
                                                     ModelProvider,
                                                     OpenAIModelProvider,
                                                     WxAIModelProvider)


class FoundationModel(BaseModel):
    model_name: Annotated[
        str | None,
        Field(
            description="The name of the foundation model.",
            default=None,
        ),
    ]
    provider: Annotated[
        ModelProvider, Field(
            description="The provider of the foundation model.")
    ]


class WxAIFoundationModel(FoundationModel):
    model_id: Annotated[
        str, Field(description="The unique identifier for the watsonx.ai model.")
    ]
    project_id: Annotated[
        str | None,
        Field(description="The project ID associated with the model.", default=None),
    ]
    space_id: Annotated[
        str | None,
        Field(description="The space ID associated with the model.", default=None),
    ]
    provider: Annotated[
        WxAIModelProvider,
        Field(
            description="The provider of the model.", default_factory=WxAIModelProvider
        ),
    ]


class OpenAIFoundationModel(FoundationModel):
    model_id: Annotated[str, Field(description="Model name from OpenAI")]
    provider: Annotated[OpenAIModelProvider, Field(
        description="OpenAI provider", default_factory=OpenAIModelProvider)]


class AzureOpenAIFoundationModel(FoundationModel):
    model_id: Annotated[str, Field(
        description="Model deployment name from Azure OpenAI")]
    provider: Annotated[AzureOpenAIModelProvider, Field(
        description="Azure OpenAI provider", default_factory=AzureOpenAIModelProvider)]


class CustomFoundationModel(FoundationModel):
    scoring_fn: Annotated[
        Callable,
        Field(
            description="A callable function that wraps the inference calls to an external LLM."
        ),
    ]
    provider: Annotated[
        ModelProvider,
        Field(
            description="The provider of the model.",
            default_factory=CustomModelProvider,
        ),
    ]
