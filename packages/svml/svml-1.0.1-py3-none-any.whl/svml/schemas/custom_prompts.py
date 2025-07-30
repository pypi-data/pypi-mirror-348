from pydantic import BaseModel, Field, field_serializer, ConfigDict
from typing import Optional, Any, Dict
import uuid

from .common import StandardLLMSettingsParams

class CustomPromptParams(BaseModel):
    """
    Parameters for the /custom endpoint of the SVML API.

    Args:
        prompt_template_id (uuid.UUID): ID of the prompt template to use.
        template_vars (Dict[str, Any], optional): Key-value pairs for template variable substitution. Defaults to an empty dict.
        settings (StandardLLMSettingsParams, optional): LLM settings.
    """
    prompt_template_id: uuid.UUID
    template_vars: Dict[str, Any] = Field(default_factory=dict)
    settings: Optional[StandardLLMSettingsParams] = None

    @field_serializer('prompt_template_id')
    def serialize_prompt_template_id(self, v: uuid.UUID):
        return str(v)

    # If you needed to support Pydantic V1 and V2 simultaneously without field_serializer,
    # or if there were multiple types, model_config with ConfigDict and json_encoders is an option.
    # However, field_serializer is cleaner for specific fields in Pydantic V2.
    # from pydantic import ConfigDict
    # model_config = ConfigDict(
    #     json_encoders={
    #         uuid.UUID: lambda v: str(v)
    #     }
    # )

class CustomPromptResponse(BaseModel):
    """
    Response from the /custom endpoint of the SVML API.
    Mirrors the StandardResponse structure from the API router.
    """
    request_id: str
    metadata: Dict[str, Any]
    result: Any # Can be string or structured data depending on post-processing
    svml_version: str
    svml_credits: int
    input: Dict[str, Any]
    output: Dict[str, Any]

    model_config = ConfigDict(extra="allow") 