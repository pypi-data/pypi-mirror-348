from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

# It's good practice to have a default model if the API provides one.
# However, for the SDK, we might not always have a direct equivalent of DEFAULT_LLM_MODEL easily accessible.
# So, we can make `model` fully optional here, and the API will apply its default if not sent.

class StandardLLMSettingsParams(BaseModel):
    """
    Standardized settings for LLM calls to be passed via the SDK.
    These settings can be passed by the client to override API defaults.
    """
    model: Optional[str] = Field(None, description="LLM model to use. See API's /models for available options. If None, API default is used.")
    svml_version: Optional[str] = Field(None, description="SVML language version to use. See API's /svml-versions for available options. If None, API default ('latest') is used.")
    max_tokens: Optional[int] = Field(None, description="Optional: Maximum number of tokens for the LLM response. Specific to certain models/providers like Anthropic.")
    # temperature: Optional[float] = Field(None, description="Optional: Sampling temperature.")
    # top_p: Optional[float] = Field(None, description="Optional: Nucleus sampling parameter.")
    # Allow other fields, similar to the API settings.
    # The API's StandardLLMSettings has `extra = 'allow'`, so the SDK can pass through extra fields.
    # Pydantic v2 uses model_config for this. Assuming Pydantic v1 based on current project structure for `extra`.
    # If using Pydantic v2, it would be:
    # model_config = {"extra": "allow"}

    model_config = ConfigDict(extra='allow') 