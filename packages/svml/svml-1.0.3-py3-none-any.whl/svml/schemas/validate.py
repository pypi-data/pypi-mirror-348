# NOTE: Endpoint logic is now handled by SVMLClient. This module only provides dataclasses.
from dataclasses import dataclass, field
from pydantic import BaseModel, ConfigDict
from typing import Optional, Any, Dict, List
import requests

class ValidateAPIRequest(BaseModel):
    """
    Parameters for the /validate API endpoint.

    Args:
        svml (str): SVML string to validate.
        svml_version (str): SVML language version to use.
        # Add any additional fields as needed

    API Mapping:
        - Python SDK: svml.schemas.validate.ValidateAPIRequest
        - API Handler: www/api-svml-dev/app/llm/validate_handler.py
        - API Router: www/api-svml-dev/app/routers/v1/validate.py
    """
    svml: str
    svml_version: str
    # Add any additional fields as needed for kwargs in client.validate
    model_config = ConfigDict(extra='allow') # To allow **kwargs from client.validate to be passed through if any

@dataclass
class ValidateResponse:
    """
    type: response

    Response from the /validate endpoint of the SVML API.

    Attributes:
        request_id (str): Unique request identifier.
        result (str): Status/result string (e.g., "SUCCESS").
        metadata (Dict[str, Any]): Metadata about the request/response.
            STRUCTURE:
                - timestamp_start (str): Request start time (ISO8601).
                - timestamp_end (str): Request end time (ISO8601).
                - time_taken (str): Time taken for the request.
                - usage (Any): Usage metadata (may be null).
                - endpoint (str): API endpoint path.
                - api_version (str): API version.
                - request_id (str): Request ID (matches top-level).
        input (Dict[str, Any]): The input parameters sent to the API.
            STRUCTURE:
                - svml (str): The SVML string submitted for validation.
                - svml_version (str): The SVML version.
        output (Dict[str, Any]): The validation results.
            STRUCTURE:
                - valid (bool): Whether the SVML is valid.
                - violations (list): List of violation objects (if any).
                - best_practices (list): List of best practice suggestions (if any).
        extra (Dict[str, Any]): Any additional fields returned by the API.

    Example:
        {
            "request_id": "...",
            "result": "SUCCESS",
            "metadata": {
                "timestamp_start": "...",
                "timestamp_end": "...",
                "time_taken": "...",
                "usage": null,
                "endpoint": "/v1/validate",
                "api_version": "v1",
                "request_id": "..."
            },
            "input": {
                "svml": "...",
                "svml_version": "1.2.2"
            },
            "output": {
                "valid": true,
                "violations": [],
                "best_practices": []
            }
        }
    """
    request_id: str
    result: str    
    metadata: Dict[str, Any]
    input: Dict[str, Any]
    output: Dict[str, Any]
    valid: bool
    errors: List[str]
    best_practices: List[str]
    svml_version: str = ''
    svml_credits: int = 0
    usage: Dict[str, Any] = field(default_factory=dict)
    extra: Dict[str, Any] = field(default_factory=dict)
    

    def __init__(self, **kwargs):
        self.request_id = kwargs.get('request_id')
        self.result = kwargs.get('result')
        self.svml_version = kwargs.get('svml_version', '')
        self.svml_credits = kwargs.get('svml_credits', 0)
        self.metadata = kwargs.get('metadata')
        self.input = kwargs.get('input')
        self.output = kwargs.get('output')
        self.valid = kwargs.get('valid')
        self.errors = kwargs.get('errors')
        self.best_practices = kwargs.get('best_practices')
        known = {'request_id', 'result', 'svml_version', 'svml_credits', 'metadata', 'input', 'output', 'valid', 'errors', 'best_practices'}
        self.extra = {k: v for k, v in kwargs.items() if k not in known}

