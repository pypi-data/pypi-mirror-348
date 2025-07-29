# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Required, TypeAlias, TypedDict

__all__ = ["BucketLocatorParam", "Bucket", "BucketBucket", "ModuleID"]


class BucketBucket(TypedDict, total=False):
    application_name: Optional[str]
    """Optional Application"""

    name: str
    """The name of the bucket"""

    version: Optional[str]
    """Optional version of the bucket"""


class Bucket(TypedDict, total=False):
    bucket: Required[BucketBucket]
    """BucketName represents a bucket name with an optional version"""


class ModuleID(TypedDict, total=False):
    module_id: Required[str]


BucketLocatorParam: TypeAlias = Union[Bucket, ModuleID]
