# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------
from types import NoneType

from ibm_watsonx_gov.entities.enums import MistakeType

# Conversion between types that may be listed in an API specification and their
# Python counterparts for tool calling hallucinations
SPEC_TYPES = {
    "any": str,
    "array": list,
    "arraylist": list,
    "bigint": int,
    "bool": bool,
    "boolean": bool,
    "byte": int,
    "char": str,
    "dict": dict,
    "double": float,
    "float": float,
    "hashtable": dict,
    "hashmap": dict,
    "integer": int,
    "int": int,
    "int64": int,
    "list": list,
    "long": int,
    "number": float,
    "null": NoneType,
    "object": dict,
    "queue": list,
    "stack": list,
    "short": int,
    "string": str,
    "tuple": tuple,
    "str": str,
}


def static_evaluate_calls(tool_specifications: list, query: str, tool_calls: list):
    """
    Perform static evaluation:
    **Static Evaluation**:
    - **Non-existent API Function**: Verifies that the API function exists in the provided API specification.
    - **Non-existent Parameter**: Checks that all parameters in the API call are valid for the specified API function.
    - **Incorrect Parameter Value Type**: Ensures that the data type of each parameter value matches the expected type.
    - **Missing Required Parameter**: Ensures all required parameters for the API function are present in the call.
    - **Hallucinated parameter**: The parameter is not valid for the selected API call.
    - **Allowed values**: The value of the parameter is not part of the allowed values mentioned in the API specification.
    - **None function**: Not able to identify the USER's intent.
    - **Invalid value**: The value is not syntactically valid for example, a string that does not have a closing quote or a list missing a bracket.
    - **Repeated parameter**: The same parameter is repeated more than once.

    Args:
        tool_specifications (list): List of tool specification
        query (str): Question/input
        tool_calls (list): List of tool calls made
    """
    API_calls_dict = []
    for call in tool_calls:
        issue = static_eval_call(tool_specifications, query, call)
        if issue:
            API_calls_dict.append(issue)
    return API_calls_dict


def static_eval_call(tool_specifications: list, query: str, call: dict):
    """
    Check for issues with inferred call.

    Returns:
        The output is returned as dictionary, which includes:
            api_call (str): The API call being validated.
            is_valid (bool): Whether the API call is valid or not.
            issues (Optional[List[Mistake]]):
                - A single mistake, if the issue relates to the entire API call (e.g., wrong API selection).
                - A list of mistakes, if multiple parameter issues exist.
                - None, if the API call is valid.
            alternative_api_call (Optional[str]): Only for parameter issues with the same API function. Suggested alternative API call without unit transformation mistakes.

    Args:
        tool_specifications (list): _description_
        query (str): _description_
        call (dict): _description_
    """
    result = {}
    if call.get("name") == "none":
        hallucination = {
            "hallucination_type": MistakeType.NONE_FUNC.value
        }
        result["value"] = 1.0
        result["hallucinations"] = [hallucination]
        result["tool_name"] = call.get("name")
        return result

    # Get Document in context that corresponds to this API call
    tool = get_details_for_call(call.get("name"), tool_specifications)

    if not tool:
        hallucination = {
            "hallucination_type": MistakeType.HALLUCINATED_CALL.value
        }
        result["value"] = 1.0
        result["hallucinations"] = [hallucination]
        result["tool_name"] = call.get("name")
        return result

    parameter_hallucinations = []
    for param in call.get("parameters"):
        # Check if parameter is part of API call
        if param not in tool.get("parameters"):
            hallucination = {
                "hallucination_type": MistakeType.HALLUCINATED_PARAM.value
            }
            parameter_hallucinations.append(hallucination)
            continue

        if "type" in tool.get("parameters")[param]:
            fix_type = (
                tool.get("parameters")[param]["type"].lower().replace(
                    ", optional", "").strip()
            )
            fix_type = fix_type.partition("[")[0]  # to fix list[int]
            # todo make a better fix
            fix_type = (
                tool.get("parameters")[param]["type"].lower().replace(
                    ", optional", "").strip()
            )
            fix_type = fix_type.partition("[")[0]  # to fix list[int]

            value_type = SPEC_TYPES[fix_type]
            value = call.get("parameters")[param]
            if not isinstance(
                value,
                value_type,
            ):
                if value_type is float:
                    call.get("parameters")[param] = float(value)
                elif value_type is int:
                    call.get("parameters")[param] = int(value)
                else:
                    hallucination = {
                        "hallucination_type": MistakeType.PARAM_TYPE.value,
                        "explanation": f"The value {value} of the parameter {param} is not {value_type} as it should be."
                    }
                    parameter_hallucinations.append(hallucination)

        # for nested types (array and dict)
        # TODO need to write something more general - that deals with greater level of nesting
        if tool.get("parameters")[param]["type"].lower() == "array":
            nested_type = "items"
        elif tool.get("parameters")[param]["type"].lower() == "dict":
            nested_type = "properties"
        else:
            nested_type = ""
        if nested_type:
            if "enum" in tool.get("parameters")[param][nested_type]:
                if tool.get("parameters")[param][nested_type]["enum"]:
                    if isinstance(value, list):
                        diff_list = list(
                            set(value)
                            - set(tool.get("parameters")[param]
                                  [nested_type]["enum"])
                        )
                    else:
                        diff_list = list(
                            set([value])
                            - set(tool.get("parameters")[param]
                                  [nested_type]["enum"])
                        )
                    if diff_list:
                        hallucination = {
                            "hallucination_type": MistakeType.ALLOWED_VALUES.value,
                            "explanation": f"Values that are not allowed in {param} are: {diff_list}"
                        }
                        parameter_hallucinations.append(hallucination)

        if "enum" in tool.get("parameters")[param]:
            if tool.get("parameters")[param]["enum"]:
                if isinstance(value, list):
                    diff_list = list(
                        set(value) - set(tool.get("parameters")[param]["enum"]))
                else:
                    diff_list = list(
                        set([value]) - set(tool.get("parameters")[param]["enum"]))
                if diff_list:
                    hallucination = {
                        "hallucination_type": MistakeType.ALLOWED_VALUES.value,
                        "explanation": f"Values that are not allowed in {param} are: {diff_list}"
                    }
                    parameter_hallucinations.append(hallucination)

    for param in tool.get("parameters"):
        if param in tool.get("parameters")["required"] and param not in call.get("parameters"):
            # Required parameter is missing
            hallucination = {
                "hallucination_type": MistakeType.REQ_PARAM_MISSING.value,
                "explanation": f"The required parameter {param} are not supplied as part of the call."
            }
            parameter_hallucinations.append(hallucination)

    if parameter_hallucinations:
        result["hallucinations"] = parameter_hallucinations
        result["value"] = 1.0
        result["tool_name"] = call.get("name")
    return result


def get_details_for_call(call_name: str, apis_specifications: list):
    """
    Given an apis_specifications , find the tool and return it.

    Args:
        call_name (str): API call name
        apis_specifications (list[dict]): APIs Specifications

    Returns:
        dict | None: dictionary for desired API call, if it exists.
    """
    for tool in apis_specifications:
        if tool.get("name") == call_name:
            return tool
    return None
