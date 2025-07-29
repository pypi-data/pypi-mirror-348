# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.webhooks.default_retrieve_secret_response import DefaultRetrieveSecretResponse

__all__ = ["DefaultResource", "AsyncDefaultResource"]


class DefaultResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DefaultResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mihairu0511/stainlessTest#accessing-raw-response-data-eg-headers
        """
        return DefaultResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DefaultResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mihairu0511/stainlessTest#with_streaming_response
        """
        return DefaultResourceWithStreamingResponse(self)

    def retrieve_secret(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DefaultRetrieveSecretResponse:
        """Get the signing secret for the default webhook endpoint.

        This is used to verify
        that webhook requests are coming from Replicate.

        Example cURL request:

        ```console
        curl -s \\
          -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
          https://api.replicate.com/v1/webhooks/default/secret
        ```

        The response will be a JSON object with a `key` property:

        ```json
        {
          "key": "..."
        }
        ```
        """
        return self._get(
            "/webhooks/default/secret",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DefaultRetrieveSecretResponse,
        )


class AsyncDefaultResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDefaultResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mihairu0511/stainlessTest#accessing-raw-response-data-eg-headers
        """
        return AsyncDefaultResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDefaultResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mihairu0511/stainlessTest#with_streaming_response
        """
        return AsyncDefaultResourceWithStreamingResponse(self)

    async def retrieve_secret(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DefaultRetrieveSecretResponse:
        """Get the signing secret for the default webhook endpoint.

        This is used to verify
        that webhook requests are coming from Replicate.

        Example cURL request:

        ```console
        curl -s \\
          -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
          https://api.replicate.com/v1/webhooks/default/secret
        ```

        The response will be a JSON object with a `key` property:

        ```json
        {
          "key": "..."
        }
        ```
        """
        return await self._get(
            "/webhooks/default/secret",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DefaultRetrieveSecretResponse,
        )


class DefaultResourceWithRawResponse:
    def __init__(self, default: DefaultResource) -> None:
        self._default = default

        self.retrieve_secret = to_raw_response_wrapper(
            default.retrieve_secret,
        )


class AsyncDefaultResourceWithRawResponse:
    def __init__(self, default: AsyncDefaultResource) -> None:
        self._default = default

        self.retrieve_secret = async_to_raw_response_wrapper(
            default.retrieve_secret,
        )


class DefaultResourceWithStreamingResponse:
    def __init__(self, default: DefaultResource) -> None:
        self._default = default

        self.retrieve_secret = to_streamed_response_wrapper(
            default.retrieve_secret,
        )


class AsyncDefaultResourceWithStreamingResponse:
    def __init__(self, default: AsyncDefaultResource) -> None:
        self._default = default

        self.retrieve_secret = async_to_streamed_response_wrapper(
            default.retrieve_secret,
        )
