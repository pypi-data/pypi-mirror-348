# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .text_result import TextResult

__all__ = ["SearchFindResponse", "Pagination"]


class Pagination(BaseModel):
    has_more: Optional[bool] = None
    """Indicates more results available. Used for infinite scroll implementation"""

    page: Optional[int] = None
    """Current page number (1-based)"""

    page_size: Optional[int] = None
    """Results per page. May be adjusted for performance"""

    total: Optional[int] = None
    """Total number of available results"""

    total_pages: Optional[int] = None
    """Total available pages. Calculated as ceil(total/page_size)"""


class SearchFindResponse(BaseModel):
    pagination: Optional[Pagination] = None
    """Pagination details for result navigation"""

    results: Optional[List[TextResult]] = None
    """Matched results with metadata"""
