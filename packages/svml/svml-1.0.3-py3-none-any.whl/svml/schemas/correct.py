# NOTE: Endpoint logic is now handled by SVMLClient. This module only provides dataclasses.
from dataclasses import dataclass
from pydantic import BaseModel, Field as PydanticField
from typing import Optional, Any, Dict
from .common import StandardLLMSettingsParams

class CorrectAPIRequest(BaseModel):
    """
    Represents the payload for a /correct API request.

    Args:
        validation_api_output (dict): Full output from the /validate endpoint.
        settings (StandardLLMSettingsParams): LLM settings for the correction task.
    """
    validation_api_output: dict
    settings: StandardLLMSettingsParams
    

@dataclass
class CorrectResponse:
    """
    type: response

    Response from the /correct endpoint of the SVML API.

    Attributes:
        request_id (str): Unique request identifier.
        result (str): Status/result string (e.g., "SUCCESS").
        svml_version (str): SVML version used.
        svml_credits (int): Usage credits consumed for the request.
        metadata (Dict[str, Any]): Metadata about the request/response.
        input (Dict[str, Any]): The input parameters sent to the API.
        output (Dict[str, Any]): The correction results.
        extra (Dict[str, Any]): Any additional fields returned by the API.
    """
    request_id: str
    result: str
    metadata: Dict[str, Any]
    input: Dict[str, Any]
    output: Dict[str, Any]
    svml_version: str = ''
    svml_credits: int = 0
    extra: Dict[str, Any] = PydanticField(default_factory=dict)

    def __init__(self, **kwargs):
        self.request_id = kwargs.get('request_id')
        self.result = kwargs.get('result')
        self.svml_version = kwargs.get('svml_version', '')
        self.svml_credits = kwargs.get('svml_credits', 0)
        self.metadata = kwargs.get('metadata')
        self.input = kwargs.get('input')
        self.output = kwargs.get('output')
        known = {'request_id', 'result', 'svml_version', 'svml_credits', 'metadata', 'input', 'output'}
        self.extra = {k: v for k, v in kwargs.items() if k not in known}
