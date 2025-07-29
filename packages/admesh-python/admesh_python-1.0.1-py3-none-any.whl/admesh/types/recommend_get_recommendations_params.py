# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["RecommendGetRecommendationsParams"]


class RecommendGetRecommendationsParams(TypedDict, total=False):
    agent_id: Required[str]

    query: Required[str]

    followup_suggestions: Optional[str]

    intent_summary: Optional[str]

    model: Optional[str]

    previous_query: Optional[str]

    session_id: Optional[str]

    summary: Optional[str]

    user_id: Optional[str]
