# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .text_result import TextResult

__all__ = ["ChunkSearchFindResponse"]


class ChunkSearchFindResponse(BaseModel):
    results: Optional[List[TextResult]] = None
    """Ordered list of relevant text segments.

    Each result includes full context and metadata
    """
