# NOTE: Endpoint logic is now handled by SVMLClient. This module only provides dataclasses.
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Any, Dict
from .common import StandardLLMSettingsParams # Import the new settings class

# For the SDK, we can maintain these distinct Param classes for user convenience,
# and the client method will construct the single RefineRequest payload for the API.

class RefineSVMLParams(BaseModel):
    """
    Parameters for direct SVML refinement via /refine endpoint of the SVML API.
    """
    svml: str = Field(..., description="SVML string to refine.")
    original_context: str = Field(..., description="The original context for the SVML.")
    user_additional_context: str = Field(..., description="Additional user context.")
    settings: StandardLLMSettingsParams = Field(..., description="LLM and refinement settings.")
    # model: str # Removed
    # svml_version: Optional[str] = None # Removed

class RefineFromGenerateParams(BaseModel):
    """
    Parameters for refinement from /generate output via /refine endpoint of the SVML API.
    """
    generate_api_output: Dict[str, Any] = Field(..., description="Output from the /generate endpoint.")
    user_additional_context: str = Field(..., description="Additional user context.")
    settings: StandardLLMSettingsParams = Field(..., description="LLM and refinement settings.")
    # model: str # Removed
    # svml_version: Optional[str] = None # Removed

class RefineFromCompareParams(BaseModel):
    """
    Parameters for refinement from /compare output via /refine endpoint of the SVML API.
    """
    compare_api_output: Dict[str, Any] = Field(..., description="Output from the /compare endpoint.")
    settings: StandardLLMSettingsParams = Field(..., description="LLM and refinement settings.")
    user_additional_context: Optional[str] = Field(None, description="Additional user context.") # This was optional in API as well if refining from compare
    # model: str # Removed
    # svml_version: Optional[str] = None # Removed

class RefineResponse(BaseModel):
    """
    type: response
    Response from the /refine endpoint of the SVML API.
    """
    request_id: str
    result: str
    metadata: Dict[str, Any]
    input: Dict[str, Any]
    output: Dict[str, Any]
    svml_version: str
    svml_credits: int

    model_config = ConfigDict(extra='allow')

