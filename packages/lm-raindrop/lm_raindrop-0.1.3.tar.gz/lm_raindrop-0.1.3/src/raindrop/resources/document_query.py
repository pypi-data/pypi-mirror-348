# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import document_query_ask_params
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
from ..types.document_query_ask_response import DocumentQueryAskResponse

__all__ = ["DocumentQueryResource", "AsyncDocumentQueryResource"]


class DocumentQueryResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DocumentQueryResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/LiquidMetal-AI/lm-raindrop-python-sdk#accessing-raw-response-data-eg-headers
        """
        return DocumentQueryResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DocumentQueryResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/LiquidMetal-AI/lm-raindrop-python-sdk#with_streaming_response
        """
        return DocumentQueryResourceWithStreamingResponse(self)

    def ask(
        self,
        *,
        bucket_location: BucketLocatorParam,
        input: str,
        object_id: str,
        request_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DocumentQueryAskResponse:
        """
        Enables natural conversational interactions with documents stored in
        SmartBuckets. This endpoint allows users to ask questions, request summaries,
        and explore document content through an intuitive conversational interface. The
        system understands context and can handle complex queries about document
        contents.

        The query system maintains conversation context throught the request_id,
        enabling follow-up questions and deep exploration of document content. It works
        across all supported file types and automatically handles multi-page documents,
        making complex file interaction as simple as having a conversation.

        The system will:

        - Maintain conversation history for context when using the same request_id
        - Process questions against file content
        - Generate contextual, relevant responses

        Document query is supported for all file types, including PDFs, images, and
        audio files.

        Args:
          bucket_location: The storage bucket containing the target document. Must be a valid, registered
              Smart Bucket. Used to identify which bucket to query against

          input: User's input or question about the document. Can be natural language questions,
              commands, or requests. The system will process this against the document content

          object_id: Document identifier within the bucket. Typically matches the storage path or
              key. Used to identify which document to chat with

          request_id: Client-provided conversation session identifier. Required for maintaining
              context in follow-up questions. We recommend using a UUID or ULID for this value

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/document_query",
            body=maybe_transform(
                {
                    "bucket_location": bucket_location,
                    "input": input,
                    "object_id": object_id,
                    "request_id": request_id,
                },
                document_query_ask_params.DocumentQueryAskParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentQueryAskResponse,
        )


class AsyncDocumentQueryResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDocumentQueryResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/LiquidMetal-AI/lm-raindrop-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncDocumentQueryResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDocumentQueryResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/LiquidMetal-AI/lm-raindrop-python-sdk#with_streaming_response
        """
        return AsyncDocumentQueryResourceWithStreamingResponse(self)

    async def ask(
        self,
        *,
        bucket_location: BucketLocatorParam,
        input: str,
        object_id: str,
        request_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DocumentQueryAskResponse:
        """
        Enables natural conversational interactions with documents stored in
        SmartBuckets. This endpoint allows users to ask questions, request summaries,
        and explore document content through an intuitive conversational interface. The
        system understands context and can handle complex queries about document
        contents.

        The query system maintains conversation context throught the request_id,
        enabling follow-up questions and deep exploration of document content. It works
        across all supported file types and automatically handles multi-page documents,
        making complex file interaction as simple as having a conversation.

        The system will:

        - Maintain conversation history for context when using the same request_id
        - Process questions against file content
        - Generate contextual, relevant responses

        Document query is supported for all file types, including PDFs, images, and
        audio files.

        Args:
          bucket_location: The storage bucket containing the target document. Must be a valid, registered
              Smart Bucket. Used to identify which bucket to query against

          input: User's input or question about the document. Can be natural language questions,
              commands, or requests. The system will process this against the document content

          object_id: Document identifier within the bucket. Typically matches the storage path or
              key. Used to identify which document to chat with

          request_id: Client-provided conversation session identifier. Required for maintaining
              context in follow-up questions. We recommend using a UUID or ULID for this value

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/document_query",
            body=await async_maybe_transform(
                {
                    "bucket_location": bucket_location,
                    "input": input,
                    "object_id": object_id,
                    "request_id": request_id,
                },
                document_query_ask_params.DocumentQueryAskParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentQueryAskResponse,
        )


class DocumentQueryResourceWithRawResponse:
    def __init__(self, document_query: DocumentQueryResource) -> None:
        self._document_query = document_query

        self.ask = to_raw_response_wrapper(
            document_query.ask,
        )


class AsyncDocumentQueryResourceWithRawResponse:
    def __init__(self, document_query: AsyncDocumentQueryResource) -> None:
        self._document_query = document_query

        self.ask = async_to_raw_response_wrapper(
            document_query.ask,
        )


class DocumentQueryResourceWithStreamingResponse:
    def __init__(self, document_query: DocumentQueryResource) -> None:
        self._document_query = document_query

        self.ask = to_streamed_response_wrapper(
            document_query.ask,
        )


class AsyncDocumentQueryResourceWithStreamingResponse:
    def __init__(self, document_query: AsyncDocumentQueryResource) -> None:
        self._document_query = document_query

        self.ask = async_to_streamed_response_wrapper(
            document_query.ask,
        )
