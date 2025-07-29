
# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------


from pydantic import BaseModel, Field
from typing_extensions import Annotated


class Node(BaseModel):
    """
    The class representing a node in an agentic application
    """
    name: Annotated[str, Field(
        description="The name of the node. This is the name with which the node is added in the app.")]
    func_name: Annotated[str, Field(
        description="The actual function name that is executed when the node is called.")]
