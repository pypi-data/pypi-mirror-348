import requests
import time
import os
import logging
import platform
import sys
import functools
import uuid
from typing import Optional, List, Dict, Any, Union
from . import __version__ as SVML_CLIENT_VERSION
from .schemas.auth import authenticate_with_api_key, fetch_metadata
from .schemas.analyze import AnalyzeAPIRequest, AnalyzeResponse, ALL_ANALYZE_DIMENSIONS
from .schemas.compare import CompareAPIRequest, CompareResponse
from .schemas.correct import CorrectAPIRequest, CorrectResponse
from .schemas.generate import GenerateAPIRequest, GenerateResponse
from .schemas.refine import RefineResponse, RefineSVMLParams, RefineFromGenerateParams, RefineFromCompareParams
from .schemas.validate import ValidateResponse, ValidateAPIRequest
from .schemas.common import StandardLLMSettingsParams
from .schemas.custom_prompts import CustomPromptParams, CustomPromptResponse
import json
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env.local")

# LOG_LEVEL-based logger setup
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO))
logger = logging.getLogger("svml.client")

SVML_CLIENT_NAME = "svml-python"
SVML_USER_AGENT = f"{SVML_CLIENT_NAME}/{SVML_CLIENT_VERSION}"

def _with_retry(func):
    """
    Decorator for retrying a function call with exponential backoff.
    Uses self.max_retries, self.initial_delay, self.exponential_backoff if present, else defaults.
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        max_retries = getattr(self, 'max_retries', 0) # 0 retries temporarily
        initial_delay = getattr(self, 'initial_delay', 0.5)
        exponential_backoff = getattr(self, 'exponential_backoff', 2.0)
        delay = initial_delay
        for attempt in range(max_retries + 1):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                if attempt < max_retries:
                    logger.warning(f"Retry {attempt+1}/{max_retries} after error: {e}")
                    time.sleep(delay)
                    delay *= exponential_backoff
                else:
                    logger.error(f"Max retries reached. Raising error: {e}")
                    raise
    return wrapper

class SVMLClient:
    """
    type: class

    SVML API client. Authenticates with auth.svml.dev and calls api.svml.dev endpoints.
    Includes retry logic and LOG_LEVEL-based logging.
    API and auth base URLs can be overridden by SVML_API_BASE and SVML_AUTH_BASE env vars.
    Only supports API key authentication.
    """
    def __init__(self, api_base=None, auth_base=None, api_key=None, max_retries=0, initial_delay=0.5, exponential_backoff=2.0, log_level=None):
        """
        Initialize the SVMLClient.

        Required Args:
            api_key (str): A valid SVML API key. You can obtain one from https://www.svml.dev.

        Optional Args:
            api_base (str, optional): Override the base URL for the SVML API. Defaults to "https://api.svml.dev".
            auth_base (str, optional): Override the base URL for authentication. Defaults to "https://auth.svml.dev".
            max_retries (int, optional): Maximum number of retries for API calls. Defaults to 2.
            initial_delay (float, optional): Initial delay (in seconds) between retries. Defaults to 0.5.
            exponential_backoff (float, optional): Backoff multiplier for retries. Defaults to 2.0.
            log_level (str, optional): Logging level (e.g., 'DEBUG', 'INFO', 'WARNING'). Can also be set via LOG_LEVEL env var. Defaults to 'INFO'.

        Notes:
            - Retry and backoff settings are also described in the `authenticate_with_api_key` method.
            - All arguments are optional except for `api_key`, which is required for authentication.
        """
        self.api_base = api_base or os.environ.get("SVML_API_BASE", "https://api.svml.dev")
        self.auth_base = auth_base or os.environ.get("SVML_AUTH_BASE", "https://auth.svml.dev")
        # Ensure /v1 is appended to base URLs
        if not self.api_base.rstrip("/").endswith("/v1"):
            self.api_base = self.api_base.rstrip("/") + "/v1"
        if not self.auth_base.rstrip("/").endswith("/v1"):
            self.auth_base = self.auth_base.rstrip("/") + "/v1"
        # Logging setup
        self.log_level = (log_level or os.environ.get("LOG_LEVEL", "INFO")).upper()
        logging.basicConfig(level=getattr(logging, self.log_level, logging.INFO))
        self.logger = logging.getLogger("svml.client")
        self.logger.setLevel(getattr(logging, self.log_level, logging.INFO))
        self.api_key = api_key or os.environ.get("SVML_API_KEY")
        self.token = None
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.exponential_backoff = exponential_backoff
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})
        self.session.mount('https://', requests.adapters.HTTPAdapter())
        self.session.mount('http://', requests.adapters.HTTPAdapter())
        self.session.log_level = self.log_level  # Save log level in session
        self.session_api = requests.Session()
        self.session_api.headers.update({'Content-Type': 'application/json'})
        self.session_api.mount('https://', requests.adapters.HTTPAdapter())
        self.session_api.mount('http://', requests.adapters.HTTPAdapter())
        self.session_api.base_url = self.api_base
        self.session.base_url = self.auth_base
        self.session_api.log_level = self.log_level  # Save log level in session_api
        # Add global client metadata headers
        self.session_api.headers.update({
            'X-Client-Name': SVML_CLIENT_NAME,
            'X-Client-Version': SVML_CLIENT_VERSION,
            'X-Platform': platform.system().lower(),
            'X-Language-Version': f'python-{platform.python_version()}',
            'X-User-Agent': SVML_USER_AGENT,
        })
        self.models = []
        self.svml_versions = []
        self.default_model = 'gpt-4.1-mini'
        self.default_svml_version = 'latest'

    def set_log_level(self, log_level):
        """
        Set the logging level for the SVML client and sessions.
        Args:
            log_level (str): Logging level (e.g., 'DEBUG', 'INFO', 'WARNING').
        """
        self.log_level = log_level.upper()
        self.logger.setLevel(getattr(logging, self.log_level, logging.INFO))
        self.session.log_level = self.log_level
        self.session_api.log_level = self.log_level

    def set_default_model(self, model):
        """
        Set the default model to use for all requests if no model is provided.
        If models are available (after authentication), validates the model.
        If models are not yet available, sets the value and validates after authentication.
        """
        if self.models:
            self._validate_model(model)
        self.default_model = model

    def set_default_svml_version(self, svml_version):
        """
        Set the default SVML version to use for all requests if no svml_version is provided.
        If svml_versions are available (after authentication), validates the version.
        If svml_versions are not yet available, sets the value and validates after authentication.
        """
        if self.svml_versions:
            self._validate_svml_version(svml_version)
        self.default_svml_version = svml_version

    @_with_retry
    def authenticate(self):
        """
        Authenticates using the API key and stores the access token. Also fetches and stores available models and SVML versions for argument validation.
        Validates the current default_model against the fetched models list.
        """
        if not self.api_key:
            raise ValueError("API key must be provided via constructor or SVML_API_KEY env var.")
        logger.debug(f"Authenticating with API key at {self.auth_base}/api-keys/validate")
        
        # Get token from auth endpoint
        self.token = authenticate_with_api_key(self.session, self.api_key, self.max_retries, self.initial_delay, self.exponential_backoff, self.auth_base)
        logger.info("API key authentication successful.")
        
        # Fetch models and SVML versions from metadata endpoints
        metadata = fetch_metadata(
            self.session_api, 
            self.token, 
            self.api_base, 
            self.max_retries, 
            self.initial_delay, 
            self.exponential_backoff
        )
        self.models = metadata.get('models', [])
        self.svml_versions = metadata.get('svml_versions', [])
        
        if self.models:
            logger.info(f"Fetched models: {self.models}")
        if self.svml_versions:
            logger.info(f"Fetched SVML versions: {self.svml_versions}")
            
        # Validate default_model
        if self.default_model and self.models:
            self._validate_model(self.default_model)
        # Validate default_svml_version
        if self.default_svml_version and self.svml_versions:
            self._validate_svml_version(self.default_svml_version)
            
        return self.token

    def _validate_model(self, model):
        if model is not None and self.models and model not in self.models:
            raise ValueError(f"Model '{model}' is not supported. Available: {self.models}")

    def _validate_svml_version(self, svml_version):
        if svml_version is not None and self.svml_versions and svml_version not in self.svml_versions:
            raise ValueError(f"SVML version '{svml_version}' is not supported. Available: {self.svml_versions}")

    @_with_retry
    def generate(self, context: str, settings: Optional[StandardLLMSettingsParams] = None, **kwargs) -> 'GenerateResponse':
        """
        Generate SVML from a given context.

        Args:
            context (str): The input context for generating SVML.
            settings (StandardLLMSettingsParams, optional): LLM and generation settings.
                If not provided, client defaults for model and svml_version will be used.
            **kwargs: Additional keyword arguments that can be part of settings (e.g., max_tokens).
                      These will be merged into the settings, overriding values in the 'settings' object if provided.

        Returns:
            GenerateResponse: The response from the /generate endpoint.
        """
        current_settings_dict = settings.model_dump(exclude_unset=True) if settings else {}
        current_settings_dict.update(kwargs) # kwargs override settings object fields

        final_settings = StandardLLMSettingsParams(**current_settings_dict)

        if final_settings.model is None:
            final_settings.model = self.default_model
        if final_settings.svml_version is None:
            final_settings.svml_version = self.default_svml_version

        self._validate_model(final_settings.model)
        self._validate_svml_version(final_settings.svml_version)

        api_request_payload = GenerateAPIRequest(context=context, settings=final_settings)
        return self._generate(api_request_payload)

    def _generate(self, payload: GenerateAPIRequest):
        response = self.session_api.post(
            f'{self.api_base}/generate',
            json=payload.model_dump(exclude_none=True),
            headers={'Authorization': f'Bearer {self.token}'}
        )
        
        response.raise_for_status()
        return GenerateResponse(**response.json())

    @_with_retry
    def validate(self, svml: str, svml_version: Optional[str] = None, **kwargs) -> 'ValidateResponse':
        """
        Validate SVML syntax and structure.

        Args:
            svml (str): The SVML text to validate.
            svml_version (str, optional): The SVML version to validate against.
                                       If None, client default (self.default_svml_version) is used.
            **kwargs: Additional keyword arguments (currently not used by the /validate endpoint but allowed for future compatibility).

        Returns:
            ValidateResponse: The response from the /validate endpoint.
        """
        resolved_svml_version = svml_version if svml_version is not None else self.default_svml_version
        self._validate_svml_version(resolved_svml_version) # Validate before sending

        # Note: /validate API does not take a 'settings' object like other endpoints.
        # It takes svml_version directly in its request schema.
        # The ValidateAPIRequest schema should reflect this.
        
        # Assuming ValidateParams is or will be the schema for the /validate request body
        # and it takes 'svml' and 'svml_version'.
        # We need to ensure that the schema file svml/schemas/validate.py defines ValidateAPIRequest correctly.
        from .schemas.validate import ValidateAPIRequest # Ensure this import exists and is correct

        api_request_payload = ValidateAPIRequest(svml=svml, svml_version=resolved_svml_version, **kwargs)
        return self._validate(api_request_payload)

    def _validate(self, payload: 'ValidateAPIRequest'): # Changed 'params' to 'payload' for consistency
        response = self.session_api.post(
            f'{self.api_base}/validate',
            json=payload.model_dump(exclude_none=True),
            headers={'Authorization': f'Bearer {self.token}'}
        )
        # if not response.json()['output']['valid']:
        #     print(f"Validate response: {json.dumps(response.json(), indent=2)}")
        response.raise_for_status()
        from .schemas.validate import ValidateResponse
        return ValidateResponse(**response.json())

    @_with_retry
    def correct(self, validate_api_output: dict, settings: Optional[StandardLLMSettingsParams] = None, **kwargs) -> 'CorrectResponse':
        """
        Correct invalid SVML based on output from the /validate endpoint.

        Args:
            validate_api_output (dict): The full JSON response from a /validate API call.
            settings (StandardLLMSettingsParams, optional): LLM and correction settings.
                                                       Client defaults are used if not provided.
            **kwargs: Additional keyword arguments for settings, overriding values in the 'settings' object.

        Returns:
            CorrectResponse: The response from the /correct endpoint.
        """
        current_settings_dict = settings.model_dump(exclude_unset=True) if settings else {}
        current_settings_dict.update(kwargs)

        final_settings = StandardLLMSettingsParams(**current_settings_dict)

        if final_settings.model is None:
            final_settings.model = self.default_model
        if final_settings.svml_version is None:
            final_settings.svml_version = self.default_svml_version

        self._validate_model(final_settings.model)
        self._validate_svml_version(final_settings.svml_version)

        api_request_payload = CorrectAPIRequest(validation_api_output=validate_api_output, settings=final_settings)
        return self._correct(api_request_payload)
        
    def _correct(self, payload: CorrectAPIRequest):
        response = self.session_api.post(
            f'{self.api_base}/correct',
            json=payload.model_dump(exclude_none=True),
            headers={'Authorization': f'Bearer {self.token}'}
        )
        response.raise_for_status()
        return CorrectResponse(**response.json())

    @_with_retry
    def compare(self, original_context: str, svml_a: str, model_a: Optional[str], svml_b: str, model_b: Optional[str], settings: Optional[StandardLLMSettingsParams] = None, **kwargs) -> 'CompareResponse':
        """
        Compare two SVML documents directly.

        Args:
            original_context (str): The original source text from which both SVMLs were derived.
            svml_a (str): The first SVML document.
            model_a (str, optional): The model that generated svml_a.
            svml_b (str): The second SVML document.
            model_b (str, optional): The model that generated svml_b.
            settings (StandardLLMSettingsParams, optional): LLM and comparison settings.
            **kwargs: Additional keyword arguments for settings.

        Returns:
            CompareResponse: The response from the /compare endpoint.
        """
        current_settings_dict = settings.model_dump(exclude_unset=True) if settings else {}
        current_settings_dict.update(kwargs)

        final_settings = StandardLLMSettingsParams(**current_settings_dict)

        if final_settings.model is None:
            final_settings.model = self.default_model
        if final_settings.svml_version is None:
            final_settings.svml_version = self.default_svml_version

        self._validate_model(final_settings.model)
        self._validate_svml_version(final_settings.svml_version)

        api_request_payload = CompareAPIRequest(
            original_context=original_context,
            svml_a=svml_a,
            model_a=model_a,
            svml_b=svml_b,
            model_b=model_b,
            settings=final_settings
            # compare_type will be set by Pydantic model in CompareAPIRequest based on these inputs
        )
        return self._compare(api_request_payload)

    def _compare(self, payload: CompareAPIRequest):
        response = self.session_api.post(
            f'{self.api_base}/compare',
            json=payload.model_dump(exclude_none=True),
            headers={'Authorization': f'Bearer {self.token}'}
        )
        response.raise_for_status()
        return CompareResponse(**response.json())

    @_with_retry
    def compareFromGenerate(self, original_context: str, generate_api_output_a: dict, generate_api_output_b: dict, settings: Optional[StandardLLMSettingsParams] = None, **kwargs) -> 'CompareResponse':
        """
        Compare two SVML documents sourced from /generate API outputs.
        The original_context will be extracted from the generate_api_output if not provided explicitly,
        but it's better to pass it if known to ensure consistency.

        Args:
            original_context (str): The original source text.
            generate_api_output_a (dict): Full JSON response from a /generate call for the first SVML.
            generate_api_output_b (dict): Full JSON response from a /generate call for the second SVML.
            settings (StandardLLMSettingsParams, optional): LLM and comparison settings.
            **kwargs: Additional keyword arguments for settings.

        Returns:
            CompareResponse: The response from the /compare endpoint.
        """
        current_settings_dict = settings.model_dump(exclude_unset=True) if settings else {}
        current_settings_dict.update(kwargs)

        final_settings = StandardLLMSettingsParams(**current_settings_dict)

        if final_settings.model is None:
            final_settings.model = self.default_model
        if final_settings.svml_version is None:
            final_settings.svml_version = self.default_svml_version

        self._validate_model(final_settings.model)
        self._validate_svml_version(final_settings.svml_version)
        
        # original_context from generate_api_output_a (or _b) input field can be used by CompareAPIRequest validator
        # if explicit original_context is not passed or is None.
        # However, the API requires original_context, so it's best to ensure it's present.

        api_request_payload = CompareAPIRequest(
            original_context=original_context,
            generate_api_output_a=generate_api_output_a,
            generate_api_output_b=generate_api_output_b,
            settings=final_settings
            # compare_type will be set by Pydantic model
        )
        return self._compare(api_request_payload)

    @_with_retry
    def refine(self, original_context: str, svml: str, user_additional_context: str, settings: Optional[StandardLLMSettingsParams] = None, **kwargs) -> 'RefineResponse':
        """
        Refine SVML based on user-provided SVML and additional context.

        Args:
            original_context (str): The original source text from which the SVML was derived.
            svml (str): The SVML to refine.
            user_additional_context (str): User's instructions or feedback for refinement.
            settings (StandardLLMSettingsParams, optional): LLM and refinement settings.
            **kwargs: Additional keyword arguments for settings.

        Returns:
            RefineResponse: The response from the /refine endpoint.
        """
        current_settings_dict = settings.model_dump(exclude_unset=True) if settings else {}
        current_settings_dict.update(kwargs)

        final_settings = StandardLLMSettingsParams(**current_settings_dict)

        if final_settings.model is None:
            final_settings.model = self.default_model
        if final_settings.svml_version is None:
            final_settings.svml_version = self.default_svml_version

        self._validate_model(final_settings.model)
        self._validate_svml_version(final_settings.svml_version)

        # RefineSVMLParams expects: svml, original_context, user_additional_context, settings
        params = RefineSVMLParams(
            svml=svml,
            original_context=original_context,
            user_additional_context=user_additional_context,
            settings=final_settings
        )
        return self._refine(params)

    @_with_retry
    def refineFromGenerate(self, generate_api_output: dict, user_additional_context: str, settings: Optional[StandardLLMSettingsParams] = None, **kwargs) -> 'RefineResponse':
        """
        Refine SVML based on a /generate API output and additional user context.

        Args:
            generate_api_output (dict): Full JSON response from a /generate API call.
            user_additional_context (str): User's instructions or feedback for refinement.
            settings (StandardLLMSettingsParams, optional): LLM and refinement settings.
            **kwargs: Additional keyword arguments for settings.

        Returns:
            RefineResponse: The response from the /refine endpoint.
        """
        current_settings_dict = settings.model_dump(exclude_unset=True) if settings else {}
        current_settings_dict.update(kwargs)

        final_settings = StandardLLMSettingsParams(**current_settings_dict)

        if final_settings.model is None:
            final_settings.model = self.default_model
        if final_settings.svml_version is None:
            final_settings.svml_version = self.default_svml_version

        self._validate_model(final_settings.model)
        self._validate_svml_version(final_settings.svml_version)

        # RefineFromGenerateParams expects: generate_api_output, user_additional_context, settings
        # original_context will be extracted by the Pydantic model if possible
        params = RefineFromGenerateParams(
            generate_api_output=generate_api_output,
            user_additional_context=user_additional_context,
            settings=final_settings
        )
        return self._refine(params)

    @_with_retry
    def refineFromCompare(self, compare_api_output: dict, svml_choice: str, user_additional_context: Optional[str] = None, settings: Optional[StandardLLMSettingsParams] = None, **kwargs) -> 'RefineResponse': # Added svml_choice
        """
        Refine SVML based on a /compare API output, user's choice, and additional context.

        Args:
            compare_api_output (dict): Full JSON response from a /compare API call.
            svml_choice (str): Indicates which SVML to refine ('A' or 'B').
            user_additional_context (str, optional): User's instructions or feedback.
            settings (StandardLLMSettingsParams, optional): LLM and refinement settings.
            **kwargs: Additional keyword arguments for settings.

        Returns:
            RefineResponse: The response from the /refine endpoint.
        """
        current_settings_dict = settings.model_dump(exclude_unset=True) if settings else {}
        current_settings_dict.update(kwargs)

        final_settings = StandardLLMSettingsParams(**current_settings_dict)

        if final_settings.model is None:
            final_settings.model = self.default_model
        if final_settings.svml_version is None:
            final_settings.svml_version = self.default_svml_version

        self._validate_model(final_settings.model)
        self._validate_svml_version(final_settings.svml_version)

        # RefineFromCompareParams expects: compare_api_output, svml_choice, user_additional_context, settings
        # original_context will be extracted by the Pydantic model if possible
        params = RefineFromCompareParams(
            compare_api_output=compare_api_output,
            svml_choice=svml_choice,
            user_additional_context=user_additional_context,
            settings=final_settings
        )
        return self._refine(params)

    def _refine(self, params: Union[RefineSVMLParams, RefineFromGenerateParams, RefineFromCompareParams]): # Added Union typing
        # The RefineParams classes (RefineSVMLParams, etc.) in svml.schemas.refine already expect 
        # a 'settings' field. The public methods above now construct these params correctly.
        # The API request model for /refine (RefineRequest in FastAPI) will internally
        # handle the different sources (svml, compare_api_output, generate_api_output)
        # based on which one is provided. The Python SDK mirrors this by passing the
        # specific Pydantic model (RefineSVMLParams, etc.) that corresponds to the chosen input type.
        # The .model_dump() will produce the correct JSON structure.

        response = self.session_api.post(
            f'{self.api_base}/refine',
            json=params.model_dump(exclude_none=True), # exclude_none is important
            headers={'Authorization': f'Bearer {self.token}'}
        )
        response.raise_for_status()
        return RefineResponse(**response.json())

    @_with_retry
    def analyze(self, svml: str, dimensions: Optional[List[str]] = None, settings: Optional[StandardLLMSettingsParams] = None, **kwargs) -> 'AnalyzeResponse':
        """
        Analyze SVML for conceptual quality.

        Args:
            svml (str): The SVML text to analyze.
            dimensions (List[str], optional): Specific dimensions to analyze (e.g., ["clarity", "coherence"]).
                                           Defaults to all dimensions if None.
            settings (StandardLLMSettingsParams, optional): LLM and analysis settings.
            **kwargs: Additional keyword arguments for settings.

        Returns:
            AnalyzeResponse: The response from the /analyze endpoint.
        """
        current_settings_dict = settings.model_dump(exclude_unset=True) if settings else {}
        current_settings_dict.update(kwargs)

        final_settings = StandardLLMSettingsParams(**current_settings_dict)

        if final_settings.model is None:
            final_settings.model = self.default_model
        if final_settings.svml_version is None:
            final_settings.svml_version = self.default_svml_version

        self._validate_model(final_settings.model)
        self._validate_svml_version(final_settings.svml_version)

        api_request_payload = AnalyzeAPIRequest(
            svml=svml,
            dimensions=dimensions if dimensions else ALL_ANALYZE_DIMENSIONS, # Send all if None
            settings=final_settings
        )
        return self._analyze(api_request_payload)

    def _analyze(self, payload: AnalyzeAPIRequest):
        response = self.session_api.post(
            f'{self.api_base}/analyze',
            json=payload.model_dump(exclude_none=True),
            headers={'Authorization': f'Bearer {self.token}'}
        )
        response.raise_for_status()
        return AnalyzeResponse(**response.json())

    @_with_retry
    def custom_prompt(self, prompt_template_id: uuid.UUID, template_vars: Optional[Dict[str, Any]] = None, settings: Optional[StandardLLMSettingsParams] = None, **kwargs) -> 'CustomPromptResponse':
        """
        Execute a custom prompt template.

        Args:
            prompt_template_id (uuid.UUID): ID of the prompt template to use.
            template_vars (Dict[str, Any], optional): Key-value pairs for template variable substitution.
            settings (StandardLLMSettingsParams, optional): LLM settings for the execution.
            **kwargs: Additional keyword arguments for settings.

        Returns:
            CustomPromptResponse: The response from the /custom endpoint.
        """
        current_settings_dict = settings.model_dump(exclude_unset=True) if settings else {}
        current_settings_dict.update(kwargs)

        final_settings = StandardLLMSettingsParams(**current_settings_dict)

        if final_settings.model is None:
            final_settings.model = self.default_model
        if final_settings.svml_version is None:
            final_settings.svml_version = self.default_svml_version
        
        self._validate_model(final_settings.model)
        self._validate_svml_version(final_settings.svml_version)

        # CustomPromptParams is the schema for the request body
        # It expects prompt_template_id, template_vars, and settings
        api_request_payload = CustomPromptParams(
            prompt_template_id=prompt_template_id,
            template_vars=template_vars if template_vars else {},
            settings=final_settings
        )
        return self._custom_prompt(api_request_payload) # Changed 'params' to 'api_request_payload'

    def _custom_prompt(self, payload: CustomPromptParams) -> CustomPromptResponse: # Changed 'params' to 'payload'
        response = self.session_api.post(
            f'{self.api_base}/custom',
            json=payload.model_dump(exclude_none=True),
            headers={'Authorization': f'Bearer {self.token}'}
        )
        response.raise_for_status()
        return CustomPromptResponse(**response.json())

__all__ = ["SVMLClient"] 