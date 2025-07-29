# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable

import httpx

from ..types import chunk_search_find_params
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
from ..types.chunk_search_find_response import ChunkSearchFindResponse

__all__ = ["ChunkSearchResource", "AsyncChunkSearchResource"]


class ChunkSearchResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ChunkSearchResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/LiquidMetal-AI/lm-raindrop-python-sdk#accessing-raw-response-data-eg-headers
        """
        return ChunkSearchResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ChunkSearchResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/LiquidMetal-AI/lm-raindrop-python-sdk#with_streaming_response
        """
        return ChunkSearchResourceWithStreamingResponse(self)

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
    ) -> ChunkSearchFindResponse:
        """
        Chunk Search provides search capabilities that serve as a complete drop-in
        replacement for traditional RAG pipelines. This system enables AI agents to
        leverage private data stored in SmartBuckets with zero additional configuration.

        Each input query is processed by our AI agent to determine the best way to
        search the data. The system will then return the most relevant results from the
        data ranked by relevance on the input query.

        Args:
          bucket_locations: The buckets to search. If provided, the search will only return results from
              these buckets

          input: Natural language query or question. Can include complex criteria and
              relationships. The system will optimize the search strategy based on this input

          request_id: Client-provided search session identifier. Required for pagination and result
              tracking. We recommend using a UUID or ULID for this value

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/chunk_search",
            body=maybe_transform(
                {
                    "bucket_locations": bucket_locations,
                    "input": input,
                    "request_id": request_id,
                },
                chunk_search_find_params.ChunkSearchFindParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChunkSearchFindResponse,
        )


class AsyncChunkSearchResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncChunkSearchResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/LiquidMetal-AI/lm-raindrop-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncChunkSearchResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncChunkSearchResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/LiquidMetal-AI/lm-raindrop-python-sdk#with_streaming_response
        """
        return AsyncChunkSearchResourceWithStreamingResponse(self)

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
    ) -> ChunkSearchFindResponse:
        """
        Chunk Search provides search capabilities that serve as a complete drop-in
        replacement for traditional RAG pipelines. This system enables AI agents to
        leverage private data stored in SmartBuckets with zero additional configuration.

        Each input query is processed by our AI agent to determine the best way to
        search the data. The system will then return the most relevant results from the
        data ranked by relevance on the input query.

        Args:
          bucket_locations: The buckets to search. If provided, the search will only return results from
              these buckets

          input: Natural language query or question. Can include complex criteria and
              relationships. The system will optimize the search strategy based on this input

          request_id: Client-provided search session identifier. Required for pagination and result
              tracking. We recommend using a UUID or ULID for this value

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/chunk_search",
            body=await async_maybe_transform(
                {
                    "bucket_locations": bucket_locations,
                    "input": input,
                    "request_id": request_id,
                },
                chunk_search_find_params.ChunkSearchFindParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChunkSearchFindResponse,
        )


class ChunkSearchResourceWithRawResponse:
    def __init__(self, chunk_search: ChunkSearchResource) -> None:
        self._chunk_search = chunk_search

        self.find = to_raw_response_wrapper(
            chunk_search.find,
        )


class AsyncChunkSearchResourceWithRawResponse:
    def __init__(self, chunk_search: AsyncChunkSearchResource) -> None:
        self._chunk_search = chunk_search

        self.find = async_to_raw_response_wrapper(
            chunk_search.find,
        )


class ChunkSearchResourceWithStreamingResponse:
    def __init__(self, chunk_search: ChunkSearchResource) -> None:
        self._chunk_search = chunk_search

        self.find = to_streamed_response_wrapper(
            chunk_search.find,
        )


class AsyncChunkSearchResourceWithStreamingResponse:
    def __init__(self, chunk_search: AsyncChunkSearchResource) -> None:
        self._chunk_search = chunk_search

        self.find = async_to_streamed_response_wrapper(
            chunk_search.find,
        )
