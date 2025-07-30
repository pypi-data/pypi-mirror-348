from typing import Dict, List, Union
import re
from ena_upload.json_parsing.characteristic import ParameterValue


def fetch_parameters(protocol_dict: Dict[str, str]) -> List[Dict[str, str]]:
    """Fetches the parameters from a protocol dictionary.

    Args:
        protocol_dict (Dict[str, str]): protocol dictionary

    Returns:
        List[Dict[str, str]]: Resulting list of parameters
    """
    parameters = []
    for protocol in protocol_dict:
        for parameter in protocol["parameters"]:
            parameters.append(
                {
                    "id": parameter["@id"],
                    "name": parameter["parameterName"]["annotationValue"],
                }
            )
    return parameters


def get_parameter_values(
    process_sequence: Dict[str, str], study_protocols_dict: Dict[str, str]
) -> Dict[str, str]:
    """Returns all parameter values from a study dictionary.

    Args:
        study_dict (Dict[str, str]): Input study dictionary

    Returns:
        Dict[str, str]: Resulting dictionary of parameter values.
    """
    param_vals = []
    parameters = fetch_parameters(study_protocols_dict)
    for process in process_sequence:
        sample_ids = [clip_off_prefix(output["@id"]) for output in process["outputs"]]
        parameter_values = [
            ParameterValue.from_dict(parameter_value, parameters)
            for parameter_value in process["parameterValues"]
        ]
        for sample_id in sample_ids:
            param_vals.append(
                {"sample_id": sample_id, "parameter_values": parameter_values}
            )
    return param_vals


def get_assay_sample_associations(assay_dict: Dict[str, str]) -> List[Dict[str, str]]:
    """Fetches the list of sample assocations in a specified assay dictionary.
    Each dictionary contains a list of input ids and output ids.

    Args:
        assay_dict (Dict[str, str]): input assay dictionary

    Returns:
        List[Dict[str, str]]: List of dictionaries with the associations
    """
    process_sequence = []
    for process in assay_dict["processSequence"]:
        input_ids = [input["@id"] for input in process["inputs"]]
        output_ids = [output["@id"] for output in process["outputs"]]
        process_sequence.append({"input": input_ids, "output": output_ids})

    return process_sequence


def clip_off_prefix(alias: Union[str, List[str]]) -> Union[str, List[str]]:
    """Clips off any prefix separated by the '/' character and returns the last subelement.
    The input can be a single String or a list of Strings.

    Args:
        alias (Union[str, List[str]]): Single alias or List of aliases

    Raises:
        TypeError: If the type of the input is anything other than a String or a list of Strings, an Exception is raised.

    Returns:
        Union[str, List[str]]: Depending on the input, returns a single String or a list of Strings.
    """
    if isinstance(alias, str):
        result = re.split("/", alias)[-1]
    elif isinstance(alias, list):
        result = []
        for item in alias:
            if isinstance(item, str):
                result.append(re.split("/", item)[-1])
            else:
                raise TypeError(
                    "The 'clip_off_prefix' function only accepts strings or a list of strings"
                )
    else:
        raise TypeError(
            "The 'clip_off_prefix' function only accepts strings or a list of strings"
        )
    return result


def get_study_id(study_dict: Dict[str, str]) -> str:
    """Fetches the study ID from the comments of a provided study dictionary

    Args:
        study_dict (Dict[str, str]): study_dictionary

    Raises:
        KeyError: Raised when the 'SEEK Study ID' comment is not found

    Returns:
        str: Resulting identifier
    """
    comment_names = [comment["name"] for comment in study_dict["comments"]]
    for study_comment in study_dict["comments"]:
        if "SEEK Study ID" not in comment_names:
            raise KeyError(
                "Bad dictionary. 'SEEK Study ID' comment is mandatory in Study."
            )
        if study_comment["name"] == "SEEK Study ID":
            return study_comment["value"]


def fetch_assay_comment_by_name(
    assay_stream: Dict[str, str], comment_name: str
) -> Dict[str, str]:
    for comment in assay_stream["comments"]:
        if comment["name"] == comment_name:
            return comment


def fetch_study_comment_by_name(
    study_dict: Dict[str, str], comment_name: str
) -> Dict[str, str]:
    for comment in study_dict["comments"]:
        if comment["name"] == comment_name:
            return comment


def fetch_assay_streams(study: Dict[str, str]) -> List[Dict[str, str]]:
    return [assay for assay in study["assays"]]


def study_publication_ids(publication_isa_json: Dict) -> List[int]:
    """Retrieves the pubmed_ids from the ISA JSON

    Args:
        publication_isa_json (Dict): Publication part of the ISA JSON dictionary

    Returns:
        List[int]: List of pubmed ID's
    """
    return ",".join([str(pub["pubMedID"]) for pub in publication_isa_json])
