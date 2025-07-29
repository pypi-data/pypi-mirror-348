# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from raindrop import Raindrop, AsyncRaindrop
from tests.utils import assert_matches_type
from raindrop.types import SummarizePageSumarizePageResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSummarizePage:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_sumarize_page(self, client: Raindrop) -> None:
        summarize_page = client.summarize_page.sumarize_page(
            page=1,
            page_size=10,
            request_id="123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(SummarizePageSumarizePageResponse, summarize_page, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_sumarize_page(self, client: Raindrop) -> None:
        response = client.summarize_page.with_raw_response.sumarize_page(
            page=1,
            page_size=10,
            request_id="123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        summarize_page = response.parse()
        assert_matches_type(SummarizePageSumarizePageResponse, summarize_page, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_sumarize_page(self, client: Raindrop) -> None:
        with client.summarize_page.with_streaming_response.sumarize_page(
            page=1,
            page_size=10,
            request_id="123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            summarize_page = response.parse()
            assert_matches_type(SummarizePageSumarizePageResponse, summarize_page, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSummarizePage:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_sumarize_page(self, async_client: AsyncRaindrop) -> None:
        summarize_page = await async_client.summarize_page.sumarize_page(
            page=1,
            page_size=10,
            request_id="123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(SummarizePageSumarizePageResponse, summarize_page, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_sumarize_page(self, async_client: AsyncRaindrop) -> None:
        response = await async_client.summarize_page.with_raw_response.sumarize_page(
            page=1,
            page_size=10,
            request_id="123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        summarize_page = await response.parse()
        assert_matches_type(SummarizePageSumarizePageResponse, summarize_page, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_sumarize_page(self, async_client: AsyncRaindrop) -> None:
        async with async_client.summarize_page.with_streaming_response.sumarize_page(
            page=1,
            page_size=10,
            request_id="123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            summarize_page = await response.parse()
            assert_matches_type(SummarizePageSumarizePageResponse, summarize_page, path=["response"])

        assert cast(Any, response.is_closed) is True
