# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from stainlesstest import Stainlesstest, AsyncStainlesstest
from stainlesstest.types.webhooks import DefaultRetrieveSecretResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDefault:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_secret(self, client: Stainlesstest) -> None:
        default = client.webhooks.default.retrieve_secret()
        assert_matches_type(DefaultRetrieveSecretResponse, default, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve_secret(self, client: Stainlesstest) -> None:
        response = client.webhooks.default.with_raw_response.retrieve_secret()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        default = response.parse()
        assert_matches_type(DefaultRetrieveSecretResponse, default, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve_secret(self, client: Stainlesstest) -> None:
        with client.webhooks.default.with_streaming_response.retrieve_secret() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            default = response.parse()
            assert_matches_type(DefaultRetrieveSecretResponse, default, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncDefault:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_secret(self, async_client: AsyncStainlesstest) -> None:
        default = await async_client.webhooks.default.retrieve_secret()
        assert_matches_type(DefaultRetrieveSecretResponse, default, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve_secret(self, async_client: AsyncStainlesstest) -> None:
        response = await async_client.webhooks.default.with_raw_response.retrieve_secret()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        default = await response.parse()
        assert_matches_type(DefaultRetrieveSecretResponse, default, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve_secret(self, async_client: AsyncStainlesstest) -> None:
        async with async_client.webhooks.default.with_streaming_response.retrieve_secret() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            default = await response.parse()
            assert_matches_type(DefaultRetrieveSecretResponse, default, path=["response"])

        assert cast(Any, response.is_closed) is True
