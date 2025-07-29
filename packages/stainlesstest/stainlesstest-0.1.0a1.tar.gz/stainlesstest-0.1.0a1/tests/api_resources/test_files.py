# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import httpx
import pytest
from respx import MockRouter

from tests.utils import assert_matches_type
from stainlesstest import Stainlesstest, AsyncStainlesstest
from stainlesstest.types import File, FileListResponse
from stainlesstest._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestFiles:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: Stainlesstest) -> None:
        file = client.files.create(
            content=b"raw file contents",
        )
        assert_matches_type(File, file, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: Stainlesstest) -> None:
        file = client.files.create(
            content=b"raw file contents",
            filename="filename",
            metadata={},
            type="type",
        )
        assert_matches_type(File, file, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: Stainlesstest) -> None:
        response = client.files.with_raw_response.create(
            content=b"raw file contents",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = response.parse()
        assert_matches_type(File, file, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: Stainlesstest) -> None:
        with client.files.with_streaming_response.create(
            content=b"raw file contents",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = response.parse()
            assert_matches_type(File, file, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: Stainlesstest) -> None:
        file = client.files.retrieve(
            "file_id",
        )
        assert_matches_type(File, file, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: Stainlesstest) -> None:
        response = client.files.with_raw_response.retrieve(
            "file_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = response.parse()
        assert_matches_type(File, file, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: Stainlesstest) -> None:
        with client.files.with_streaming_response.retrieve(
            "file_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = response.parse()
            assert_matches_type(File, file, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: Stainlesstest) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `file_id` but received ''"):
            client.files.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: Stainlesstest) -> None:
        file = client.files.list()
        assert_matches_type(FileListResponse, file, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: Stainlesstest) -> None:
        response = client.files.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = response.parse()
        assert_matches_type(FileListResponse, file, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: Stainlesstest) -> None:
        with client.files.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = response.parse()
            assert_matches_type(FileListResponse, file, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: Stainlesstest) -> None:
        file = client.files.delete(
            "file_id",
        )
        assert file is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: Stainlesstest) -> None:
        response = client.files.with_raw_response.delete(
            "file_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = response.parse()
        assert file is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: Stainlesstest) -> None:
        with client.files.with_streaming_response.delete(
            "file_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = response.parse()
            assert file is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: Stainlesstest) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `file_id` but received ''"):
            client.files.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_download(self, client: Stainlesstest, respx_mock: MockRouter) -> None:
        respx_mock.get("/files/file_id/download").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        file = client.files.download(
            file_id="file_id",
            expiry=0,
            owner="owner",
            signature="signature",
        )
        assert file.is_closed
        assert file.json() == {"foo": "bar"}
        assert cast(Any, file.is_closed) is True
        assert isinstance(file, BinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_download(self, client: Stainlesstest, respx_mock: MockRouter) -> None:
        respx_mock.get("/files/file_id/download").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        file = client.files.with_raw_response.download(
            file_id="file_id",
            expiry=0,
            owner="owner",
            signature="signature",
        )

        assert file.is_closed is True
        assert file.http_request.headers.get("X-Stainless-Lang") == "python"
        assert file.json() == {"foo": "bar"}
        assert isinstance(file, BinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_download(self, client: Stainlesstest, respx_mock: MockRouter) -> None:
        respx_mock.get("/files/file_id/download").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.files.with_streaming_response.download(
            file_id="file_id",
            expiry=0,
            owner="owner",
            signature="signature",
        ) as file:
            assert not file.is_closed
            assert file.http_request.headers.get("X-Stainless-Lang") == "python"

            assert file.json() == {"foo": "bar"}
            assert cast(Any, file.is_closed) is True
            assert isinstance(file, StreamedBinaryAPIResponse)

        assert cast(Any, file.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_download(self, client: Stainlesstest) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `file_id` but received ''"):
            client.files.with_raw_response.download(
                file_id="",
                expiry=0,
                owner="owner",
                signature="signature",
            )


class TestAsyncFiles:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncStainlesstest) -> None:
        file = await async_client.files.create(
            content=b"raw file contents",
        )
        assert_matches_type(File, file, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncStainlesstest) -> None:
        file = await async_client.files.create(
            content=b"raw file contents",
            filename="filename",
            metadata={},
            type="type",
        )
        assert_matches_type(File, file, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncStainlesstest) -> None:
        response = await async_client.files.with_raw_response.create(
            content=b"raw file contents",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = await response.parse()
        assert_matches_type(File, file, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncStainlesstest) -> None:
        async with async_client.files.with_streaming_response.create(
            content=b"raw file contents",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = await response.parse()
            assert_matches_type(File, file, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncStainlesstest) -> None:
        file = await async_client.files.retrieve(
            "file_id",
        )
        assert_matches_type(File, file, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncStainlesstest) -> None:
        response = await async_client.files.with_raw_response.retrieve(
            "file_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = await response.parse()
        assert_matches_type(File, file, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncStainlesstest) -> None:
        async with async_client.files.with_streaming_response.retrieve(
            "file_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = await response.parse()
            assert_matches_type(File, file, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncStainlesstest) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `file_id` but received ''"):
            await async_client.files.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncStainlesstest) -> None:
        file = await async_client.files.list()
        assert_matches_type(FileListResponse, file, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncStainlesstest) -> None:
        response = await async_client.files.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = await response.parse()
        assert_matches_type(FileListResponse, file, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncStainlesstest) -> None:
        async with async_client.files.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = await response.parse()
            assert_matches_type(FileListResponse, file, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncStainlesstest) -> None:
        file = await async_client.files.delete(
            "file_id",
        )
        assert file is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncStainlesstest) -> None:
        response = await async_client.files.with_raw_response.delete(
            "file_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = await response.parse()
        assert file is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncStainlesstest) -> None:
        async with async_client.files.with_streaming_response.delete(
            "file_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = await response.parse()
            assert file is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncStainlesstest) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `file_id` but received ''"):
            await async_client.files.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_download(self, async_client: AsyncStainlesstest, respx_mock: MockRouter) -> None:
        respx_mock.get("/files/file_id/download").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        file = await async_client.files.download(
            file_id="file_id",
            expiry=0,
            owner="owner",
            signature="signature",
        )
        assert file.is_closed
        assert await file.json() == {"foo": "bar"}
        assert cast(Any, file.is_closed) is True
        assert isinstance(file, AsyncBinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_download(self, async_client: AsyncStainlesstest, respx_mock: MockRouter) -> None:
        respx_mock.get("/files/file_id/download").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        file = await async_client.files.with_raw_response.download(
            file_id="file_id",
            expiry=0,
            owner="owner",
            signature="signature",
        )

        assert file.is_closed is True
        assert file.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await file.json() == {"foo": "bar"}
        assert isinstance(file, AsyncBinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_download(self, async_client: AsyncStainlesstest, respx_mock: MockRouter) -> None:
        respx_mock.get("/files/file_id/download").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.files.with_streaming_response.download(
            file_id="file_id",
            expiry=0,
            owner="owner",
            signature="signature",
        ) as file:
            assert not file.is_closed
            assert file.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await file.json() == {"foo": "bar"}
            assert cast(Any, file.is_closed) is True
            assert isinstance(file, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, file.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_download(self, async_client: AsyncStainlesstest) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `file_id` but received ''"):
            await async_client.files.with_raw_response.download(
                file_id="",
                expiry=0,
                owner="owner",
                signature="signature",
            )
