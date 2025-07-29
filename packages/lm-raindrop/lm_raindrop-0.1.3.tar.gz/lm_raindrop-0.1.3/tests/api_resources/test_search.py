# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from raindrop import Raindrop, AsyncRaindrop
from tests.utils import assert_matches_type
from raindrop.types import SearchFindResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSearch:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_find(self, client: Raindrop) -> None:
        search = client.search.find(
            bucket_locations=[{"bucket": {}}],
            input="Show me documents containing credit card numbers or social security numbers",
            request_id="123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(SearchFindResponse, search, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_find(self, client: Raindrop) -> None:
        response = client.search.with_raw_response.find(
            bucket_locations=[{"bucket": {}}],
            input="Show me documents containing credit card numbers or social security numbers",
            request_id="123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = response.parse()
        assert_matches_type(SearchFindResponse, search, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_find(self, client: Raindrop) -> None:
        with client.search.with_streaming_response.find(
            bucket_locations=[{"bucket": {}}],
            input="Show me documents containing credit card numbers or social security numbers",
            request_id="123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = response.parse()
            assert_matches_type(SearchFindResponse, search, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSearch:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_find(self, async_client: AsyncRaindrop) -> None:
        search = await async_client.search.find(
            bucket_locations=[{"bucket": {}}],
            input="Show me documents containing credit card numbers or social security numbers",
            request_id="123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(SearchFindResponse, search, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_find(self, async_client: AsyncRaindrop) -> None:
        response = await async_client.search.with_raw_response.find(
            bucket_locations=[{"bucket": {}}],
            input="Show me documents containing credit card numbers or social security numbers",
            request_id="123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = await response.parse()
        assert_matches_type(SearchFindResponse, search, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_find(self, async_client: AsyncRaindrop) -> None:
        async with async_client.search.with_streaming_response.find(
            bucket_locations=[{"bucket": {}}],
            input="Show me documents containing credit card numbers or social security numbers",
            request_id="123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = await response.parse()
            assert_matches_type(SearchFindResponse, search, path=["response"])

        assert cast(Any, response.is_closed) is True
