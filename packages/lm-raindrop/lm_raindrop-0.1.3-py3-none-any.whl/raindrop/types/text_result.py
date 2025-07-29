# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["TextResult", "Source", "SourceBucket"]


class SourceBucket(BaseModel):
    application_name: Optional[str] = None

    application_version_id: Optional[str] = None

    bucket_name: Optional[str] = None

    module_id: Optional[str] = None


class Source(BaseModel):
    bucket: Optional[SourceBucket] = None
    """The bucket information containing this result"""

    object: Optional[str] = None
    """The object key within the bucket"""


class TextResult(BaseModel):
    chunk_signature: Optional[str] = None
    """Unique identifier for this text segment.

    Used for deduplication and result tracking
    """

    embed: Optional[str] = None
    """Vector representation for similarity matching.

    Used in semantic search operations
    """

    payload_signature: Optional[str] = None
    """Parent document identifier. Links related content chunks together"""

    score: Optional[float] = None
    """Relevance score (0.0 to 1.0). Higher scores indicate better matches"""

    source: Optional[Source] = None
    """Source document references. Contains bucket and object information"""

    text: Optional[str] = None
    """The actual content of the result. May be a document excerpt or full content"""

    type: Optional[str] = None
    """Content MIME type. Helps with proper result rendering"""
