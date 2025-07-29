# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------


class WatsonXGovernanceEvaluator():
    """
         Class responsible to trigger build time evaluations
    """

    def __init__(self, config: dict, credentials={}):
        self.config = config
        self.__validate_inputs()

    def __validate_inputs(self):
        pass

    def evaluate(self):
        pass
