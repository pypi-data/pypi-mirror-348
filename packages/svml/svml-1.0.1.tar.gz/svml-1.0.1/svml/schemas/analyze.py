# NOTE: Endpoint logic is now handled by SVMLClient. This module only provides dataclasses.
from dataclasses import dataclass, field
from pydantic import BaseModel, Field as PydanticField
from typing import Optional, Any, Dict, List
from enum import Enum
from .common import StandardLLMSettingsParams

class AnalyzeDimension(str, Enum):
    COGNITIVE_DIVERGENCE = "cognitive_divergence"
    COMPRESSION_SIGNATURE = "compression_signature"
    METAPHOR_ANCHORING = "metaphor_anchoring"
    PROMPT_FORM_ALIGNMENT = "prompt_form_alignment"
    AUTHOR_TRACE = "author_trace"
    AMBIGUITY_RESOLUTION = "ambiguity_resolution"

ALL_ANALYZE_DIMENSIONS = [d.value for d in AnalyzeDimension]

class AnalyzeAPIRequest(BaseModel):
    """
    Represents the payload for an /analyze API request.

    Args:
        svml (str): SVML string to analyze.
        dimensions (List[str], optional): List of analysis dimensions.
        settings (StandardLLMSettingsParams): LLM and analysis settings.

    API Mapping:
        - Python SDK Internal: svml.schemas.analyze.AnalyzeAPIRequest
        - API Handler: www/api-svml-dev/app/llm/analyze_handler.py (expects AnalyzeRequest which includes settings)
        - API Router: www/api-svml-dev/app/routers/v1/analyze.py (expects AnalyzeRequest which includes settings)
    """
    svml: str
    dimensions: Optional[List[str]] = None
    settings: StandardLLMSettingsParams

@dataclass
class AnalyzeResponse:
    """
    type: response

    Response from the /analyze endpoint of the SVML API.

    Attributes:
        overall_score (float): Overall score from the analysis (average of all dimension scores).
        verdict (str): High-level verdict/result string (e.g., "authentic").
        narrative (str): Narrative explanation of the analysis.
        dimensions (Dict[str, Any]): Detailed analysis by dimension.
            STRUCTURE:
                - <dimension_name> (dict): Results for each requested dimension (see AnalyzeDimension enum).
                    - score (float): Score for this dimension.
                    - primary_finding (str): Summary of the main finding for this dimension.
                    - scoring_details (dict): Detailed breakdown, varies by dimension, but may include:
                        - dimension_analyses (dict): Sub-analyses for the dimension.
                        - statistics (dict): Stats for the dimension (e.g., ambiguous/resolved terms).
                        - well_resolved_examples (dict): Examples of resolved ambiguities.
                        - unresolved_examples (dict): Examples of unresolved ambiguities.
                        - improvement_suggestions (dict): Suggestions for improvement.
        svml_credits (int): Credits used for the analysis.
        extra (Dict[str, Any]): Any additional fields returned by the API.

    Example:
        {
            "overall_score": 0.86,
            "verdict": "authentic",
            "narrative": "The SVML document was analyzed across 6 dimensions. Verdict: authentic. Overall score: 0.86.",
            "dimensions": {
                "cognitive_divergence": {
                    "score": 0.85,
                    "primary_finding": "...",
                    "scoring_details": {
                        "dimension_analyses": {
                            "dimension": [
                                {
                                    "@name": "concept_sequence_variations",
                                    "analysis": "...",
                                    "evidence": ["...", "..."]
                                }
                            ]
                        },
                        "score": "0.85",
                        "primary_finding": "..."
                    }
                },
                "compression_signature": {
                    "score": 0.85,
                    "primary_finding": "...",
                    "scoring_details": { ... }
                }
            },
            "svml_credits": 100
        }

    Notes:
        - The available analysis dimensions are defined in the `AnalyzeDimension` enum in svml.endpoints.analyze:
            - "cognitive_divergence"
            - "compression_signature"
            - "metaphor_anchoring"
            - "prompt_form_alignment"
            - "author_trace"
            - "ambiguity_resolution"
        - If no dimensions are specified, all available dimensions will be analyzed by default.
        - The structure of `scoring_details` may vary by dimension.
    """
    overall_score: float
    verdict: str
    narrative: str
    dimensions: Dict[str, Any]
    svml_credits: int = 0
    svml_version: str = ""
    extra: Dict[str, Any] = PydanticField(default_factory=dict)

    def __init__(self, **kwargs):
        self.overall_score = kwargs.get('overall_score')
        self.verdict = kwargs.get('verdict')
        self.narrative = kwargs.get('narrative')
        self.dimensions = kwargs.get('dimensions')
        self.svml_credits = kwargs.get('svml_credits', 0)
        known = {'overall_score', 'verdict', 'narrative', 'dimensions', 'svml_credits'}
        self.extra = {k: v for k, v in kwargs.items() if k not in known}


