# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .bucket_locator_param import BucketLocatorParam

__all__ = ["DocumentQueryAskParams"]


class DocumentQueryAskParams(TypedDict, total=False):
    bucket_location: Required[BucketLocatorParam]
    """The storage bucket containing the target document.

    Must be a valid, registered Smart Bucket. Used to identify which bucket to query
    against
    """

    input: Required[str]
    """User's input or question about the document.

    Can be natural language questions, commands, or requests. The system will
    process this against the document content
    """

    object_id: Required[str]
    """Document identifier within the bucket.

    Typically matches the storage path or key. Used to identify which document to
    chat with
    """

    request_id: Required[str]
    """Client-provided conversation session identifier.

    Required for maintaining context in follow-up questions. We recommend using a
    UUID or ULID for this value
    """
