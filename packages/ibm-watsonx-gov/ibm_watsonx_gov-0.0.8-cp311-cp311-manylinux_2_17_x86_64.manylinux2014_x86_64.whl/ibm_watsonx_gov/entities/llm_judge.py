# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------

from typing import Annotated, Union

from pydantic import BaseModel, Field

from ibm_watsonx_gov.entities.foundation_model import (
    AzureOpenAIFoundationModel, OpenAIFoundationModel, WxAIFoundationModel)


class LLMJudge(BaseModel):
    model: Annotated[Union[WxAIFoundationModel, OpenAIFoundationModel, AzureOpenAIFoundationModel], Field(
        description="The foundation model to be used as judge")]
