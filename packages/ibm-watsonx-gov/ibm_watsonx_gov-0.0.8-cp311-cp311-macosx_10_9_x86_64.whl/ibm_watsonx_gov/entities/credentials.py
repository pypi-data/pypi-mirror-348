# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------

import os
from typing import Annotated

from pydantic import BaseModel, Field

from ibm_watsonx_gov.utils.python_utils import get_environment_variable_value
from ibm_watsonx_gov.utils.url_mapping import WOS_URL_MAPPING


class Credentials(BaseModel):
    api_key: Annotated[str, Field(title="Api Key",
                                  description="The user api key.",
                                  strip_whitespace=True)]
    url: Annotated[str, Field(title="watsonx.governance url",
                              description="The watsonx.governance url. By default the url for dallas region is used.",
                              default="https://api.aiopenscale.cloud.ibm.com")]
    service_instance_id:  Annotated[str | None, Field(title="Service instance id",
                                                      description="The watsonx.governance service instance id.",
                                                      default=None)]
    username: Annotated[str | None, Field(title="User name",
                                          description="The user name.",
                                          default=None)]
    version: Annotated[str | None, Field(title="Version",
                                         description="The watsonx.governance version.",
                                         default=None)]
    disable_ssl: Annotated[bool, Field(title="Disable ssl",
                                       description="The flag to disable ssl.",
                                       default=False)]
    dai_url: Annotated[str, Field(title="watsonx.ai platform url",
                                 description="The watsonx.ai platform url. Defaults to None. This is required for users without a valid watsonx.governance instance.",
                                 default=None)]

    @classmethod
    def create_from_env(cls):
        # possible API key environment variable names
        api_key = get_environment_variable_value(
            ["WXG_API_KEY", "WATSONX_APIKEY"])

        if not api_key:
            raise ValueError("Missing API key environment variable")

        username = get_environment_variable_value(
            ["WXG_USERNAME", "WATSONX_USERNAME"])

        version = get_environment_variable_value(
            ["WXG_VERSION", "WATSONX_VERSION"])

        return Credentials(
            api_key=api_key,
            url=os.getenv("WXG_URL", "https://api.aiopenscale.cloud.ibm.com"),
            service_instance_id=os.getenv("WXG_SERVICE_INSTANCE_ID"),
            username=username,
            version=version,
            disable_ssl=os.getenv("WXG_DISABLE_SSL", False)
        )


class WxAICredentials(BaseModel):
    url: Annotated[str, Field(
        title="watsonx.ai url",
        description="The url for watsonx ai service",
        default="https://us-south.ml.cloud.ibm.com",
        examples=[
            "https://us-south.ml.cloud.ibm.com",
            "https://eu-de.ml.cloud.ibm.com",
            "https://eu-gb.ml.cloud.ibm.com",
            "https://jp-tok.ml.cloud.ibm.com",
            "https://au-syd.ml.cloud.ibm.com",
        ]
    )]
    api_key: Annotated[str, Field(title="Api Key",
                                  description="The user api key.",
                                  strip_whitespace=True)]
    version: Annotated[str | None, Field(title="Version",
                                         description="The watsonx.ai version.",
                                         default=None)]
    username: Annotated[str | None, Field(title="User name",
                                          description="The user name.",
                                          default=None)]

    @classmethod
    def create_from_env(cls):
        # possible API key environment variable names
        api_key = get_environment_variable_value(
            ["WXAI_API_KEY", "WATSONX_APIKEY", "WXG_API_KEY"])

        if not api_key:
            raise ValueError("Missing API key environment variable")

        username = get_environment_variable_value(
            ["WXAI_USERNAME", "WATSONX_USERNAME", "WXG_USERNAME"])

        version = get_environment_variable_value(
            ["WXAI_VERSION", "WATSONX_VERSION", "WXG_VERSION"])

        url = get_environment_variable_value(
            ["WXAI_URL", "WATSONX_URL", "WXG_URL"])

        # Check the url & update it
        if url in WOS_URL_MAPPING.keys():
            url = WOS_URL_MAPPING.get(url).wml_url

        # If the url environment variable is not found, use the default
        if not url:
            url = "https://us-south.ml.cloud.ibm.com"

        credentials = {
            "url": url,
            "api_key": api_key,
            "version": version,
            "username": username,
        }

        return WxAICredentials(
            **credentials
        )


class WxGovConsoleCredentials(BaseModel):
    url: str
    username: str
    password: str
    api_key: str | None = None

    @classmethod
    def create_from_env(cls):
        return WxGovConsoleCredentials(
            url=os.getenv("WXGC_URL"),
            username=os.getenv("WXGC_USERNAME"),
            password=os.getenv("WXGC_PASSWORD"),
            api_key=os.getenv("WXGC_API_KEY"),
        )


class OpenAICredentials(BaseModel):
    url: str | None
    api_key: str | None

    @classmethod
    def create_from_env(cls):
        return OpenAICredentials(
            url=os.getenv("OPENAI_URL"),
            api_key=os.getenv("OPENAI_API_KEY"),
        )


class AzureOpenAICredentials(BaseModel):
    url: Annotated[str | None, Field(
        description="Azure OpenAI url. This attribute can be read from `AZURE_OPENAI_HOST` environment variable.",
        serialization_alias="azure_openai_host")]
    api_key: Annotated[str | None, Field(
        description="API key for Azure OpenAI. This attribute can be read from `AZURE_OPENAI_API_KEY` environment variable.")]
    api_version: Annotated[str | None, Field(
        description="The model API version from Azure OpenAI. This attribute can be read from `AZURE_OPENAI_API_VERSION` environment variable.")]

    @classmethod
    def create_from_env(cls):
        return AzureOpenAICredentials(
            url=os.getenv("AZURE_OPENAI_HOST"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        )
