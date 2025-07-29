# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["RecommendGetRecommendationsResponse", "DecisionFactors", "Intent", "Response", "ResponseRecommendation"]


class DecisionFactors(BaseModel):
    highlighted: Optional[List[str]] = None

    reasoning: Optional[str] = None


class Intent(BaseModel):
    category: Optional[str] = None

    goal: Optional[List[str]] = None

    intent_match_score: Optional[float] = None

    known_mentions: Optional[List[str]] = None

    type: Optional[str] = None


class ResponseRecommendation(BaseModel):
    ad_id: str

    admesh_link: str

    admesh_trust_score: float

    product_id: str

    reason: str

    title: str

    features: Optional[List[str]] = None

    has_free_tier: Optional[bool] = None

    integrations: Optional[List[str]] = None

    pricing: Optional[str] = None

    product_match_score: Optional[float] = None

    redirect_url: Optional[str] = None

    reviews_summary: Optional[str] = None

    reward_note: Optional[str] = None

    security: Optional[List[str]] = None

    slug: Optional[str] = None

    support: Optional[List[str]] = None

    trial_days: Optional[int] = None

    url: Optional[str] = None


class Response(BaseModel):
    final_verdict: Optional[str] = None

    followup_suggestions: Optional[List[str]] = None

    recommendations: Optional[List[ResponseRecommendation]] = None

    summary: Optional[str] = None


class RecommendGetRecommendationsResponse(BaseModel):
    decision_factors: Optional[DecisionFactors] = None

    end_of_session: Optional[bool] = None

    intent: Optional[Intent] = None

    api_model_used: Optional[str] = FieldInfo(alias="model_used", default=None)

    recommendation_id: Optional[str] = None

    response: Optional[Response] = None

    session_id: Optional[str] = None

    tokens_used: Optional[int] = None
