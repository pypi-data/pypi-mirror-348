# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from stainlesstest import Stainlesstest, AsyncStainlesstest
from stainlesstest.types.models import SchemasTraining

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestVersions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: Stainlesstest) -> None:
        version = client.models.versions.retrieve(
            version_id="version_id",
            model_owner="model_owner",
            model_name="model_name",
        )
        assert version is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: Stainlesstest) -> None:
        response = client.models.versions.with_raw_response.retrieve(
            version_id="version_id",
            model_owner="model_owner",
            model_name="model_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        version = response.parse()
        assert version is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: Stainlesstest) -> None:
        with client.models.versions.with_streaming_response.retrieve(
            version_id="version_id",
            model_owner="model_owner",
            model_name="model_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            version = response.parse()
            assert version is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: Stainlesstest) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_owner` but received ''"):
            client.models.versions.with_raw_response.retrieve(
                version_id="version_id",
                model_owner="",
                model_name="model_name",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_name` but received ''"):
            client.models.versions.with_raw_response.retrieve(
                version_id="version_id",
                model_owner="model_owner",
                model_name="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version_id` but received ''"):
            client.models.versions.with_raw_response.retrieve(
                version_id="",
                model_owner="model_owner",
                model_name="model_name",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: Stainlesstest) -> None:
        version = client.models.versions.list(
            model_name="model_name",
            model_owner="model_owner",
        )
        assert version is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: Stainlesstest) -> None:
        response = client.models.versions.with_raw_response.list(
            model_name="model_name",
            model_owner="model_owner",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        version = response.parse()
        assert version is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: Stainlesstest) -> None:
        with client.models.versions.with_streaming_response.list(
            model_name="model_name",
            model_owner="model_owner",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            version = response.parse()
            assert version is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_list(self, client: Stainlesstest) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_owner` but received ''"):
            client.models.versions.with_raw_response.list(
                model_name="model_name",
                model_owner="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_name` but received ''"):
            client.models.versions.with_raw_response.list(
                model_name="",
                model_owner="model_owner",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: Stainlesstest) -> None:
        version = client.models.versions.delete(
            version_id="version_id",
            model_owner="model_owner",
            model_name="model_name",
        )
        assert version is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: Stainlesstest) -> None:
        response = client.models.versions.with_raw_response.delete(
            version_id="version_id",
            model_owner="model_owner",
            model_name="model_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        version = response.parse()
        assert version is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: Stainlesstest) -> None:
        with client.models.versions.with_streaming_response.delete(
            version_id="version_id",
            model_owner="model_owner",
            model_name="model_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            version = response.parse()
            assert version is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: Stainlesstest) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_owner` but received ''"):
            client.models.versions.with_raw_response.delete(
                version_id="version_id",
                model_owner="",
                model_name="model_name",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_name` but received ''"):
            client.models.versions.with_raw_response.delete(
                version_id="version_id",
                model_owner="model_owner",
                model_name="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version_id` but received ''"):
            client.models.versions.with_raw_response.delete(
                version_id="",
                model_owner="model_owner",
                model_name="model_name",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_create_training(self, client: Stainlesstest) -> None:
        version = client.models.versions.create_training(
            version_id="version_id",
            model_owner="model_owner",
            model_name="model_name",
            destination="destination",
            input={},
        )
        assert_matches_type(SchemasTraining, version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_training_with_all_params(self, client: Stainlesstest) -> None:
        version = client.models.versions.create_training(
            version_id="version_id",
            model_owner="model_owner",
            model_name="model_name",
            destination="destination",
            input={},
            webhook="webhook",
            webhook_events_filter=["start"],
        )
        assert_matches_type(SchemasTraining, version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create_training(self, client: Stainlesstest) -> None:
        response = client.models.versions.with_raw_response.create_training(
            version_id="version_id",
            model_owner="model_owner",
            model_name="model_name",
            destination="destination",
            input={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        version = response.parse()
        assert_matches_type(SchemasTraining, version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create_training(self, client: Stainlesstest) -> None:
        with client.models.versions.with_streaming_response.create_training(
            version_id="version_id",
            model_owner="model_owner",
            model_name="model_name",
            destination="destination",
            input={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            version = response.parse()
            assert_matches_type(SchemasTraining, version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_create_training(self, client: Stainlesstest) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_owner` but received ''"):
            client.models.versions.with_raw_response.create_training(
                version_id="version_id",
                model_owner="",
                model_name="model_name",
                destination="destination",
                input={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_name` but received ''"):
            client.models.versions.with_raw_response.create_training(
                version_id="version_id",
                model_owner="model_owner",
                model_name="",
                destination="destination",
                input={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version_id` but received ''"):
            client.models.versions.with_raw_response.create_training(
                version_id="",
                model_owner="model_owner",
                model_name="model_name",
                destination="destination",
                input={},
            )


class TestAsyncVersions:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncStainlesstest) -> None:
        version = await async_client.models.versions.retrieve(
            version_id="version_id",
            model_owner="model_owner",
            model_name="model_name",
        )
        assert version is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncStainlesstest) -> None:
        response = await async_client.models.versions.with_raw_response.retrieve(
            version_id="version_id",
            model_owner="model_owner",
            model_name="model_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        version = await response.parse()
        assert version is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncStainlesstest) -> None:
        async with async_client.models.versions.with_streaming_response.retrieve(
            version_id="version_id",
            model_owner="model_owner",
            model_name="model_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            version = await response.parse()
            assert version is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncStainlesstest) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_owner` but received ''"):
            await async_client.models.versions.with_raw_response.retrieve(
                version_id="version_id",
                model_owner="",
                model_name="model_name",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_name` but received ''"):
            await async_client.models.versions.with_raw_response.retrieve(
                version_id="version_id",
                model_owner="model_owner",
                model_name="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version_id` but received ''"):
            await async_client.models.versions.with_raw_response.retrieve(
                version_id="",
                model_owner="model_owner",
                model_name="model_name",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncStainlesstest) -> None:
        version = await async_client.models.versions.list(
            model_name="model_name",
            model_owner="model_owner",
        )
        assert version is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncStainlesstest) -> None:
        response = await async_client.models.versions.with_raw_response.list(
            model_name="model_name",
            model_owner="model_owner",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        version = await response.parse()
        assert version is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncStainlesstest) -> None:
        async with async_client.models.versions.with_streaming_response.list(
            model_name="model_name",
            model_owner="model_owner",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            version = await response.parse()
            assert version is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_list(self, async_client: AsyncStainlesstest) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_owner` but received ''"):
            await async_client.models.versions.with_raw_response.list(
                model_name="model_name",
                model_owner="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_name` but received ''"):
            await async_client.models.versions.with_raw_response.list(
                model_name="",
                model_owner="model_owner",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncStainlesstest) -> None:
        version = await async_client.models.versions.delete(
            version_id="version_id",
            model_owner="model_owner",
            model_name="model_name",
        )
        assert version is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncStainlesstest) -> None:
        response = await async_client.models.versions.with_raw_response.delete(
            version_id="version_id",
            model_owner="model_owner",
            model_name="model_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        version = await response.parse()
        assert version is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncStainlesstest) -> None:
        async with async_client.models.versions.with_streaming_response.delete(
            version_id="version_id",
            model_owner="model_owner",
            model_name="model_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            version = await response.parse()
            assert version is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncStainlesstest) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_owner` but received ''"):
            await async_client.models.versions.with_raw_response.delete(
                version_id="version_id",
                model_owner="",
                model_name="model_name",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_name` but received ''"):
            await async_client.models.versions.with_raw_response.delete(
                version_id="version_id",
                model_owner="model_owner",
                model_name="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version_id` but received ''"):
            await async_client.models.versions.with_raw_response.delete(
                version_id="",
                model_owner="model_owner",
                model_name="model_name",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_training(self, async_client: AsyncStainlesstest) -> None:
        version = await async_client.models.versions.create_training(
            version_id="version_id",
            model_owner="model_owner",
            model_name="model_name",
            destination="destination",
            input={},
        )
        assert_matches_type(SchemasTraining, version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_training_with_all_params(self, async_client: AsyncStainlesstest) -> None:
        version = await async_client.models.versions.create_training(
            version_id="version_id",
            model_owner="model_owner",
            model_name="model_name",
            destination="destination",
            input={},
            webhook="webhook",
            webhook_events_filter=["start"],
        )
        assert_matches_type(SchemasTraining, version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create_training(self, async_client: AsyncStainlesstest) -> None:
        response = await async_client.models.versions.with_raw_response.create_training(
            version_id="version_id",
            model_owner="model_owner",
            model_name="model_name",
            destination="destination",
            input={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        version = await response.parse()
        assert_matches_type(SchemasTraining, version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create_training(self, async_client: AsyncStainlesstest) -> None:
        async with async_client.models.versions.with_streaming_response.create_training(
            version_id="version_id",
            model_owner="model_owner",
            model_name="model_name",
            destination="destination",
            input={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            version = await response.parse()
            assert_matches_type(SchemasTraining, version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_create_training(self, async_client: AsyncStainlesstest) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_owner` but received ''"):
            await async_client.models.versions.with_raw_response.create_training(
                version_id="version_id",
                model_owner="",
                model_name="model_name",
                destination="destination",
                input={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `model_name` but received ''"):
            await async_client.models.versions.with_raw_response.create_training(
                version_id="version_id",
                model_owner="model_owner",
                model_name="",
                destination="destination",
                input={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version_id` but received ''"):
            await async_client.models.versions.with_raw_response.create_training(
                version_id="",
                model_owner="model_owner",
                model_name="model_name",
                destination="destination",
                input={},
            )
