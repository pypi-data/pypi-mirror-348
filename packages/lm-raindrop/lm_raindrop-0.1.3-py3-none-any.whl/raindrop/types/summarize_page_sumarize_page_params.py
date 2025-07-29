# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["SummarizePageSumarizePageParams"]


class SummarizePageSumarizePageParams(TypedDict, total=False):
    page: Required[int]
    """Target page number (1-based)"""

    page_size: Required[int]
    """Results per page. Affects summary granularity"""

    request_id: Required[str]
    """Original search session identifier from the initial search"""
