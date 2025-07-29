# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable

import httpx

from ..types import search_find_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.bucket_locator_param import BucketLocatorParam
from ..types.search_find_response import SearchFindResponse

__all__ = ["SearchResource", "AsyncSearchResource"]


class SearchResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SearchResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/LiquidMetal-AI/lm-raindrop-python-sdk#accessing-raw-response-data-eg-headers
        """
        return SearchResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SearchResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/LiquidMetal-AI/lm-raindrop-python-sdk#with_streaming_response
        """
        return SearchResourceWithStreamingResponse(self)

    def find(
        self,
        *,
        bucket_locations: Iterable[BucketLocatorParam],
        input: str,
        request_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SearchFindResponse:
        """
        Primary search endpoint that provides advanced search capabilities across all
        document types stored in SmartBuckets.

        Supports recursive object search within objects, enabling nested content search
        like embedded images, text content, and personally identifiable information
        (PII).

        The system supports complex queries like:

        - 'Show me documents containing credit card numbers or social security numbers'
        - 'Find images of landscapes taken during sunset'
        - 'Get documents mentioning revenue forecasts from Q4 2023'
        - 'Find me all PDF documents that contain pictures of a cat'
        - 'Find me all audio files that contain information about the weather in SF in
          2024'

        Key capabilities:

        - Natural language query understanding
        - Content-based search across text, images, and audio
        - Automatic PII detection
        - Multi-modal search (text, images, audio)

        Args:
          bucket_locations: The buckets to search. If provided, the search will only return results from
              these buckets

          input: Natural language search query that can include complex criteria. Supports
              queries like finding documents with specific content types, PII, or semantic
              meaning

          request_id: Client-provided search session identifier. Required for pagination and result
              tracking. We recommend using a UUID or ULID for this value

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/search",
            body=maybe_transform(
                {
                    "bucket_locations": bucket_locations,
                    "input": input,
                    "request_id": request_id,
                },
                search_find_params.SearchFindParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SearchFindResponse,
        )


class AsyncSearchResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSearchResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/LiquidMetal-AI/lm-raindrop-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncSearchResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSearchResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/LiquidMetal-AI/lm-raindrop-python-sdk#with_streaming_response
        """
        return AsyncSearchResourceWithStreamingResponse(self)

    async def find(
        self,
        *,
        bucket_locations: Iterable[BucketLocatorParam],
        input: str,
        request_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SearchFindResponse:
        """
        Primary search endpoint that provides advanced search capabilities across all
        document types stored in SmartBuckets.

        Supports recursive object search within objects, enabling nested content search
        like embedded images, text content, and personally identifiable information
        (PII).

        The system supports complex queries like:

        - 'Show me documents containing credit card numbers or social security numbers'
        - 'Find images of landscapes taken during sunset'
        - 'Get documents mentioning revenue forecasts from Q4 2023'
        - 'Find me all PDF documents that contain pictures of a cat'
        - 'Find me all audio files that contain information about the weather in SF in
          2024'

        Key capabilities:

        - Natural language query understanding
        - Content-based search across text, images, and audio
        - Automatic PII detection
        - Multi-modal search (text, images, audio)

        Args:
          bucket_locations: The buckets to search. If provided, the search will only return results from
              these buckets

          input: Natural language search query that can include complex criteria. Supports
              queries like finding documents with specific content types, PII, or semantic
              meaning

          request_id: Client-provided search session identifier. Required for pagination and result
              tracking. We recommend using a UUID or ULID for this value

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/search",
            body=await async_maybe_transform(
                {
                    "bucket_locations": bucket_locations,
                    "input": input,
                    "request_id": request_id,
                },
                search_find_params.SearchFindParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SearchFindResponse,
        )


class SearchResourceWithRawResponse:
    def __init__(self, search: SearchResource) -> None:
        self._search = search

        self.find = to_raw_response_wrapper(
            search.find,
        )


class AsyncSearchResourceWithRawResponse:
    def __init__(self, search: AsyncSearchResource) -> None:
        self._search = search

        self.find = async_to_raw_response_wrapper(
            search.find,
        )


class SearchResourceWithStreamingResponse:
    def __init__(self, search: SearchResource) -> None:
        self._search = search

        self.find = to_streamed_response_wrapper(
            search.find,
        )


class AsyncSearchResourceWithStreamingResponse:
    def __init__(self, search: AsyncSearchResource) -> None:
        self._search = search

        self.find = async_to_streamed_response_wrapper(
            search.find,
        )
