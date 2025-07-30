# NOTE: Endpoint logic is now handled by SVMLClient. This module only provides dataclasses.
from dataclasses import dataclass
from pydantic import BaseModel
from typing import Optional, Any, Dict
from .common import StandardLLMSettingsParams

class GenerateAPIRequest(BaseModel):
    """
    Represents the payload for a /generate API request.

    Args:
        context (str): Natural language context to convert to SVML.
        settings (StandardLLMSettingsParams): LLM and generation settings.
        # Add any additional fields as needed for the API payload structure

    API Mapping:
        - Python SDK Internal: svml.schemas.generate.GenerateAPIRequest
        - API Handler: www/api-svml-dev/app/llm/generate_handler.py (expects GenerateRequest which includes settings)
        - API Router: www/api-svml-dev/app/routers/v1/generate.py (expects GenerateRequest which includes settings)
    """
    context: str
    settings: StandardLLMSettingsParams
    # svml_version: str # Removed, now in settings
    # model: str      # Removed, now in settings
    # Add any additional fields as needed

@dataclass
class GenerateResponse:
    """
    type: response

    Response from the /generate endpoint of the SVML API.

    Attributes:
        request_id (str): Unique request identifier.
        result (str): Status/result string (e.g., "SUCCESS").
        svml_version (str): The SVML language version used.
        svml_credits (int): Number of SVML credits used by this request
        metadata (Dict[str, Any]): Metadata about the request/response.
            STRUCTURE:
                - provider (str): LLM provider (e.g., "openai").
                - model (str): Model used for generation.
                - timestamp_start (str): Request start time (ISO8601).
                - timestamp_end (str): Request end time (ISO8601).
                - time_taken (str): Time taken for the request.
                - endpoint (str): API endpoint path.
                - api_version (str): API version.
                - request_id (str): Request ID (matches top-level).
                - HTTP_status (int): HTTP status code.
        input (Dict[str, Any]): The input parameters sent to the API.
            STRUCTURE:
                - context (str): The original prompt/context.
                - svml_version (str): SVML version requested.
                - model (str): LLM Model requested for generating SVML
        output (Dict[str, Any]): The generated SVML and justifications.
            STRUCTURE:
                - svml (str): The generated SVML string.
                - justifications (str): Justification text for the SVML in MD format

    Example:
        {
            "request_id": "...",
            "metadata": {
                "provider": "openai",
                "model": "gpt-4.1-mini",
                "timestamp_start": "...",
                "timestamp_end": "...",
                "time_taken": "...",
                "endpoint": "/v1/generate",
                "api_version": "v1",
                "request_id": "...",
                "HTTP_status": 200
            },
            "result": "SUCCESS",
            "svml_version": "1.2.1",
            "svml_credits": 4391,
            "input": {
                "context": "...",
                "svml_version": "1.2.1",
                "model": "gpt-4.1-mini"
            },
            "output": {
                "svml": "...",
                "justifications": "..."
            }
        }
    """
    request_id: str
    result: str
    svml_version: str
    svml_credits: int
    metadata: Dict[str, Any]
    input: Dict[str, Any]
    output: Dict[str, Any]
    extra: Dict[str, Any] = None

    def __init__(self, **kwargs):
        self.request_id = kwargs.get('request_id')
        self.result = kwargs.get('result')
        self.svml_version = kwargs.get('svml_version')
        self.svml_credits = kwargs.get('svml_credits')
        self.metadata = kwargs.get('metadata')
        self.input = kwargs.get('input')
        self.output = kwargs.get('output')
        known = {'request_id', 'result', 'svml_version', 'svml_credits', 'metadata', 'input', 'output'}
        self.extra = {k: v for k, v in kwargs.items() if k not in known}

