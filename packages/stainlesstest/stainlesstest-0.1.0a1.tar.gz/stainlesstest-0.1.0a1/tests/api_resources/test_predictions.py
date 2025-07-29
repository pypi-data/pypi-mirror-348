# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from stainlesstest import Stainlesstest, AsyncStainlesstest
from stainlesstest.types import (
    PredictionResponse,
    PredictionListResponse,
)
from stainlesstest._utils import parse_datetime

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPredictions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: Stainlesstest) -> None:
        prediction = client.predictions.create(
            input={},
            version="version",
        )
        assert_matches_type(PredictionResponse, prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: Stainlesstest) -> None:
        prediction = client.predictions.create(
            input={},
            version="version",
            stream=True,
            webhook="webhook",
            webhook_events_filter=["start"],
            prefer="wait=5",
        )
        assert_matches_type(PredictionResponse, prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: Stainlesstest) -> None:
        response = client.predictions.with_raw_response.create(
            input={},
            version="version",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prediction = response.parse()
        assert_matches_type(PredictionResponse, prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: Stainlesstest) -> None:
        with client.predictions.with_streaming_response.create(
            input={},
            version="version",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prediction = response.parse()
            assert_matches_type(PredictionResponse, prediction, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: Stainlesstest) -> None:
        prediction = client.predictions.retrieve(
            "prediction_id",
        )
        assert_matches_type(PredictionResponse, prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: Stainlesstest) -> None:
        response = client.predictions.with_raw_response.retrieve(
            "prediction_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prediction = response.parse()
        assert_matches_type(PredictionResponse, prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: Stainlesstest) -> None:
        with client.predictions.with_streaming_response.retrieve(
            "prediction_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prediction = response.parse()
            assert_matches_type(PredictionResponse, prediction, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: Stainlesstest) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `prediction_id` but received ''"):
            client.predictions.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: Stainlesstest) -> None:
        prediction = client.predictions.list()
        assert_matches_type(PredictionListResponse, prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: Stainlesstest) -> None:
        prediction = client.predictions.list(
            created_after=parse_datetime("2025-01-01T00:00:00Z"),
            created_before=parse_datetime("2025-02-01T00:00:00Z"),
        )
        assert_matches_type(PredictionListResponse, prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: Stainlesstest) -> None:
        response = client.predictions.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prediction = response.parse()
        assert_matches_type(PredictionListResponse, prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: Stainlesstest) -> None:
        with client.predictions.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prediction = response.parse()
            assert_matches_type(PredictionListResponse, prediction, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_cancel(self, client: Stainlesstest) -> None:
        prediction = client.predictions.cancel(
            "prediction_id",
        )
        assert_matches_type(PredictionResponse, prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_cancel(self, client: Stainlesstest) -> None:
        response = client.predictions.with_raw_response.cancel(
            "prediction_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prediction = response.parse()
        assert_matches_type(PredictionResponse, prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_cancel(self, client: Stainlesstest) -> None:
        with client.predictions.with_streaming_response.cancel(
            "prediction_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prediction = response.parse()
            assert_matches_type(PredictionResponse, prediction, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_cancel(self, client: Stainlesstest) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `prediction_id` but received ''"):
            client.predictions.with_raw_response.cancel(
                "",
            )


class TestAsyncPredictions:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncStainlesstest) -> None:
        prediction = await async_client.predictions.create(
            input={},
            version="version",
        )
        assert_matches_type(PredictionResponse, prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncStainlesstest) -> None:
        prediction = await async_client.predictions.create(
            input={},
            version="version",
            stream=True,
            webhook="webhook",
            webhook_events_filter=["start"],
            prefer="wait=5",
        )
        assert_matches_type(PredictionResponse, prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncStainlesstest) -> None:
        response = await async_client.predictions.with_raw_response.create(
            input={},
            version="version",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prediction = await response.parse()
        assert_matches_type(PredictionResponse, prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncStainlesstest) -> None:
        async with async_client.predictions.with_streaming_response.create(
            input={},
            version="version",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prediction = await response.parse()
            assert_matches_type(PredictionResponse, prediction, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncStainlesstest) -> None:
        prediction = await async_client.predictions.retrieve(
            "prediction_id",
        )
        assert_matches_type(PredictionResponse, prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncStainlesstest) -> None:
        response = await async_client.predictions.with_raw_response.retrieve(
            "prediction_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prediction = await response.parse()
        assert_matches_type(PredictionResponse, prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncStainlesstest) -> None:
        async with async_client.predictions.with_streaming_response.retrieve(
            "prediction_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prediction = await response.parse()
            assert_matches_type(PredictionResponse, prediction, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncStainlesstest) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `prediction_id` but received ''"):
            await async_client.predictions.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncStainlesstest) -> None:
        prediction = await async_client.predictions.list()
        assert_matches_type(PredictionListResponse, prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncStainlesstest) -> None:
        prediction = await async_client.predictions.list(
            created_after=parse_datetime("2025-01-01T00:00:00Z"),
            created_before=parse_datetime("2025-02-01T00:00:00Z"),
        )
        assert_matches_type(PredictionListResponse, prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncStainlesstest) -> None:
        response = await async_client.predictions.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prediction = await response.parse()
        assert_matches_type(PredictionListResponse, prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncStainlesstest) -> None:
        async with async_client.predictions.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prediction = await response.parse()
            assert_matches_type(PredictionListResponse, prediction, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_cancel(self, async_client: AsyncStainlesstest) -> None:
        prediction = await async_client.predictions.cancel(
            "prediction_id",
        )
        assert_matches_type(PredictionResponse, prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_cancel(self, async_client: AsyncStainlesstest) -> None:
        response = await async_client.predictions.with_raw_response.cancel(
            "prediction_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prediction = await response.parse()
        assert_matches_type(PredictionResponse, prediction, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_cancel(self, async_client: AsyncStainlesstest) -> None:
        async with async_client.predictions.with_streaming_response.cancel(
            "prediction_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prediction = await response.parse()
            assert_matches_type(PredictionResponse, prediction, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_cancel(self, async_client: AsyncStainlesstest) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `prediction_id` but received ''"):
            await async_client.predictions.with_raw_response.cancel(
                "",
            )
