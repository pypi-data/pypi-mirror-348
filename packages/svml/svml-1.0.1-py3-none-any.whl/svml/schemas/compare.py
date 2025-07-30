# NOTE: Endpoint logic is now handled by SVMLClient. This module only provides dataclasses.
from pydantic import BaseModel, Field, model_validator, ConfigDict
from typing import Optional, Any, Dict
from .common import StandardLLMSettingsParams # Import the new settings class
import logging # Added import

logger = logging.getLogger(__name__) # Added logger instance

class CompareAPIRequest(BaseModel):
    """
    Parameters for the /compare endpoint of the SVML API.

    Args:
        original_context (str): The original source text.
        settings (StandardLLMSettingsParams): LLM settings for the comparison task itself.
        svml_a (str, optional): SVML A string. Provide with svml_b for direct SVML comparison.
        svml_b (str, optional): SVML B string. Provide with svml_a for direct SVML comparison.
        generate_api_output_a (dict, optional): Full output from first /generate endpoint call. Provide with generate_api_output_b.
        generate_api_output_b (dict, optional): Full output from second /generate endpoint call. Provide with generate_api_output_a.
    """
    original_context: str = Field(..., description="The original source text.")
    settings: StandardLLMSettingsParams = Field(..., description="LLM settings for the comparison task itself.")
    
    # Option 1: Direct SVMLs
    svml_a: Optional[str] = Field(None, description="First SVML document to compare.")
    svml_b: Optional[str] = Field(None, description="Second SVML document to compare.")
    
    # Option 2: Full /generate outputs
    generate_api_output_a: Optional[Dict[str, Any]] = Field(None, description="Full output from first /generate endpoint call.")
    generate_api_output_b: Optional[Dict[str, Any]] = Field(None, description="Full output from second /generate endpoint call.")

    @model_validator(mode='after')
    def check_inputs(cls, values):
        svml_a, svml_b = values.svml_a, values.svml_b
        gen_a, gen_b = values.generate_api_output_a, values.generate_api_output_b

        using_direct_svml = bool(svml_a or svml_b)
        using_generate_outputs = bool(gen_a or gen_b)

        if using_direct_svml and using_generate_outputs:
            raise ValueError("Cannot provide both direct SVMLs (svml_a/b) and generate_api_outputs (generate_api_output_a/b) simultaneously.")
        
        if not using_direct_svml and not using_generate_outputs:
            raise ValueError("Must provide either (svml_a, svml_b) or (generate_api_output_a, generate_api_output_b).")

        if using_direct_svml:
            if not (svml_a and svml_b):
                raise ValueError("If using direct SVML input, both svml_a and svml_b must be provided.")
        
        if using_generate_outputs:
            if not (gen_a and gen_b):
                raise ValueError("If using generate_api_outputs, both generate_api_output_a and generate_api_output_b must be provided.")
            # Context validation for generate_outputs can also be done here or in the API handler
            context_a = gen_a.get('input', {}).get('context')
            context_b = gen_b.get('input', {}).get('context')
            if values.original_context and context_a and values.original_context != context_a:
                 logger.warning("original_context provided does not match context in generate_api_output_a")
            if values.original_context and context_b and values.original_context != context_b:
                 logger.warning("original_context provided does not match context in generate_api_output_b")

        return values

class CompareResponse(BaseModel):
    """
    type: response
    Response from the /compare endpoint of the SVML API.
    """
    request_id: str
    result: str
    metadata: Dict[str, Any]
    input: Dict[str, Any]
    output: Dict[str, Any]
    svml_version: str
    svml_credits: int

    model_config = ConfigDict(extra='allow')

