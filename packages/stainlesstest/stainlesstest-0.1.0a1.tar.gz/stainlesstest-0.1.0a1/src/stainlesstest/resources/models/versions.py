# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.models import version_create_training_params
from ...types.models.schemas_training import SchemasTraining

__all__ = ["VersionsResource", "AsyncVersionsResource"]


class VersionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> VersionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mihairu0511/stainlessTest#accessing-raw-response-data-eg-headers
        """
        return VersionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> VersionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mihairu0511/stainlessTest#with_streaming_response
        """
        return VersionsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        version_id: str,
        *,
        model_owner: str,
        model_name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Example cURL request:

        ```console
        curl -s \\
          -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
          https://api.replicate.com/v1/models/replicate/hello-world/versions/5c7d5dc6dd8bf75c1acaa8565735e7986bc5b66206b55cca93cb72c9bf15ccaa
        ```

        The response will be the version object:

        ```json
        {
          "id": "5c7d5dc6dd8bf75c1acaa8565735e7986bc5b66206b55cca93cb72c9bf15ccaa",
          "created_at": "2022-04-26T19:29:04.418669Z",
          "cog_version": "0.3.0",
          "openapi_schema": {...}
        }
        ```

        Every model describes its inputs and outputs with
        [OpenAPI Schema Objects](https://spec.openapis.org/oas/latest.html#schemaObject)
        in the `openapi_schema` property.

        The `openapi_schema.components.schemas.Input` property for the
        [replicate/hello-world](https://replicate.com/replicate/hello-world) model looks
        like this:

        ```json
        {
          "type": "object",
          "title": "Input",
          "required": ["text"],
          "properties": {
            "text": {
              "x-order": 0,
              "type": "string",
              "title": "Text",
              "description": "Text to prefix with 'hello '"
            }
          }
        }
        ```

        The `openapi_schema.components.schemas.Output` property for the
        [replicate/hello-world](https://replicate.com/replicate/hello-world) model looks
        like this:

        ```json
        {
          "type": "string",
          "title": "Output"
        }
        ```

        For more details, see the docs on
        [Cog's supported input and output types](https://github.com/replicate/cog/blob/75b7802219e7cd4cee845e34c4c22139558615d4/docs/python.md#input-and-output-types)

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_owner:
            raise ValueError(f"Expected a non-empty value for `model_owner` but received {model_owner!r}")
        if not model_name:
            raise ValueError(f"Expected a non-empty value for `model_name` but received {model_name!r}")
        if not version_id:
            raise ValueError(f"Expected a non-empty value for `version_id` but received {version_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/models/{model_owner}/{model_name}/versions/{version_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def list(
        self,
        model_name: str,
        *,
        model_owner: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Example cURL request:

        ```console
        curl -s \\
          -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
          https://api.replicate.com/v1/models/replicate/hello-world/versions
        ```

        The response will be a JSON array of model version objects, sorted with the most
        recent version first:

        ```json
        {
          "next": null,
          "previous": null,
          "results": [
            {
              "id": "5c7d5dc6dd8bf75c1acaa8565735e7986bc5b66206b55cca93cb72c9bf15ccaa",
              "created_at": "2022-04-26T19:29:04.418669Z",
              "cog_version": "0.3.0",
              "openapi_schema": {...}
            }
          ]
        }
        ```

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_owner:
            raise ValueError(f"Expected a non-empty value for `model_owner` but received {model_owner!r}")
        if not model_name:
            raise ValueError(f"Expected a non-empty value for `model_name` but received {model_name!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/models/{model_owner}/{model_name}/versions",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def delete(
        self,
        version_id: str,
        *,
        model_owner: str,
        model_name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete a model version and all associated predictions, including all output
        files.

        Model version deletion has some restrictions:

        - You can only delete versions from models you own.
        - You can only delete versions from private models.
        - You cannot delete a version if someone other than you has run predictions with
          it.
        - You cannot delete a version if it is being used as the base model for a fine
          tune/training.
        - You cannot delete a version if it has an associated deployment.
        - You cannot delete a version if another model version is overridden to use it.

        Example cURL request:

        ```command
        curl -s -X DELETE \\
          -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
          https://api.replicate.com/v1/models/replicate/hello-world/versions/5c7d5dc6dd8bf75c1acaa8565735e7986bc5b66206b55cca93cb72c9bf15ccaa
        ```

        The response will be an empty 202, indicating the deletion request has been
        accepted. It might take a few minutes to be processed.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_owner:
            raise ValueError(f"Expected a non-empty value for `model_owner` but received {model_owner!r}")
        if not model_name:
            raise ValueError(f"Expected a non-empty value for `model_name` but received {model_name!r}")
        if not version_id:
            raise ValueError(f"Expected a non-empty value for `version_id` but received {version_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/models/{model_owner}/{model_name}/versions/{version_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def create_training(
        self,
        version_id: str,
        *,
        model_owner: str,
        model_name: str,
        destination: str,
        input: object,
        webhook: str | NotGiven = NOT_GIVEN,
        webhook_events_filter: List[Literal["start", "output", "logs", "completed"]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SchemasTraining:
        """
        Start a new training of the model version you specify.

        Example request body:

        ```json
        {
          "destination": "{new_owner}/{new_name}",
          "input": {
            "train_data": "https://example.com/my-input-images.zip"
          },
          "webhook": "https://example.com/my-webhook"
        }
        ```

        Example cURL request:

        ```console
        curl -s -X POST \\
          -d '{"destination": "{new_owner}/{new_name}", "input": {"input_images": "https://example.com/my-input-images.zip"}}' \\
          -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
          -H 'Content-Type: application/json' \\
          https://api.replicate.com/v1/models/stability-ai/sdxl/versions/da77bc59ee60423279fd632efb4795ab731d9e3ca9705ef3341091fb989b7eaf/trainings
        ```

        The response will be the training object:

        ```json
        {
          "id": "zz4ibbonubfz7carwiefibzgga",
          "model": "stability-ai/sdxl",
          "version": "da77bc59ee60423279fd632efb4795ab731d9e3ca9705ef3341091fb989b7eaf",
          "input": {
            "input_images": "https://example.com/my-input-images.zip"
          },
          "logs": "",
          "error": null,
          "status": "starting",
          "created_at": "2023-09-08T16:32:56.990893084Z",
          "urls": {
            "cancel": "https://api.replicate.com/v1/predictions/zz4ibbonubfz7carwiefibzgga/cancel",
            "get": "https://api.replicate.com/v1/predictions/zz4ibbonubfz7carwiefibzgga"
          }
        }
        ```

        As models can take several minutes or more to train, the result will not be
        available immediately. To get the final result of the training you should either
        provide a `webhook` HTTPS URL for us to call when the results are ready, or poll
        the [get a training](#trainings.get) endpoint until it has finished.

        When a training completes, it creates a new
        [version](https://replicate.com/docs/how-does-replicate-work#terminology) of the
        model at the specified destination.

        To find some models to train on, check out the
        [trainable language models collection](https://replicate.com/collections/trainable-language-models).

        Args:
          destination: A string representing the desired model to push to in the format
              `{destination_model_owner}/{destination_model_name}`. This should be an existing
              model owned by the user or organization making the API request. If the
              destination is invalid, the server will return an appropriate 4XX response.

          input: An object containing inputs to the Cog model's `train()` function.

          webhook: An HTTPS URL for receiving a webhook when the training completes. The webhook
              will be a POST request where the request body is the same as the response body
              of the [get training](#trainings.get) operation. If there are network problems,
              we will retry the webhook a few times, so make sure it can be safely called more
              than once. Replicate will not follow redirects when sending webhook requests to
              your service, so be sure to specify a URL that will resolve without redirecting.

          webhook_events_filter: By default, we will send requests to your webhook URL whenever there are new
              outputs or the training has finished. You can change which events trigger
              webhook requests by specifying `webhook_events_filter` in the training request:

              - `start`: immediately on training start
              - `output`: each time a training generates an output (note that trainings can
                generate multiple outputs)
              - `logs`: each time log output is generated by a training
              - `completed`: when the training reaches a terminal state
                (succeeded/canceled/failed)

              For example, if you only wanted requests to be sent at the start and end of the
              training, you would provide:

              ```json
              {
                "destination": "my-organization/my-model",
                "input": {
                  "text": "Alice"
                },
                "webhook": "https://example.com/my-webhook",
                "webhook_events_filter": ["start", "completed"]
              }
              ```

              Requests for event types `output` and `logs` will be sent at most once every
              500ms. If you request `start` and `completed` webhooks, then they'll always be
              sent regardless of throttling.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_owner:
            raise ValueError(f"Expected a non-empty value for `model_owner` but received {model_owner!r}")
        if not model_name:
            raise ValueError(f"Expected a non-empty value for `model_name` but received {model_name!r}")
        if not version_id:
            raise ValueError(f"Expected a non-empty value for `version_id` but received {version_id!r}")
        return self._post(
            f"/models/{model_owner}/{model_name}/versions/{version_id}/trainings",
            body=maybe_transform(
                {
                    "destination": destination,
                    "input": input,
                    "webhook": webhook,
                    "webhook_events_filter": webhook_events_filter,
                },
                version_create_training_params.VersionCreateTrainingParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SchemasTraining,
        )


class AsyncVersionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncVersionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mihairu0511/stainlessTest#accessing-raw-response-data-eg-headers
        """
        return AsyncVersionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncVersionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mihairu0511/stainlessTest#with_streaming_response
        """
        return AsyncVersionsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        version_id: str,
        *,
        model_owner: str,
        model_name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Example cURL request:

        ```console
        curl -s \\
          -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
          https://api.replicate.com/v1/models/replicate/hello-world/versions/5c7d5dc6dd8bf75c1acaa8565735e7986bc5b66206b55cca93cb72c9bf15ccaa
        ```

        The response will be the version object:

        ```json
        {
          "id": "5c7d5dc6dd8bf75c1acaa8565735e7986bc5b66206b55cca93cb72c9bf15ccaa",
          "created_at": "2022-04-26T19:29:04.418669Z",
          "cog_version": "0.3.0",
          "openapi_schema": {...}
        }
        ```

        Every model describes its inputs and outputs with
        [OpenAPI Schema Objects](https://spec.openapis.org/oas/latest.html#schemaObject)
        in the `openapi_schema` property.

        The `openapi_schema.components.schemas.Input` property for the
        [replicate/hello-world](https://replicate.com/replicate/hello-world) model looks
        like this:

        ```json
        {
          "type": "object",
          "title": "Input",
          "required": ["text"],
          "properties": {
            "text": {
              "x-order": 0,
              "type": "string",
              "title": "Text",
              "description": "Text to prefix with 'hello '"
            }
          }
        }
        ```

        The `openapi_schema.components.schemas.Output` property for the
        [replicate/hello-world](https://replicate.com/replicate/hello-world) model looks
        like this:

        ```json
        {
          "type": "string",
          "title": "Output"
        }
        ```

        For more details, see the docs on
        [Cog's supported input and output types](https://github.com/replicate/cog/blob/75b7802219e7cd4cee845e34c4c22139558615d4/docs/python.md#input-and-output-types)

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_owner:
            raise ValueError(f"Expected a non-empty value for `model_owner` but received {model_owner!r}")
        if not model_name:
            raise ValueError(f"Expected a non-empty value for `model_name` but received {model_name!r}")
        if not version_id:
            raise ValueError(f"Expected a non-empty value for `version_id` but received {version_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/models/{model_owner}/{model_name}/versions/{version_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def list(
        self,
        model_name: str,
        *,
        model_owner: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Example cURL request:

        ```console
        curl -s \\
          -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
          https://api.replicate.com/v1/models/replicate/hello-world/versions
        ```

        The response will be a JSON array of model version objects, sorted with the most
        recent version first:

        ```json
        {
          "next": null,
          "previous": null,
          "results": [
            {
              "id": "5c7d5dc6dd8bf75c1acaa8565735e7986bc5b66206b55cca93cb72c9bf15ccaa",
              "created_at": "2022-04-26T19:29:04.418669Z",
              "cog_version": "0.3.0",
              "openapi_schema": {...}
            }
          ]
        }
        ```

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_owner:
            raise ValueError(f"Expected a non-empty value for `model_owner` but received {model_owner!r}")
        if not model_name:
            raise ValueError(f"Expected a non-empty value for `model_name` but received {model_name!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/models/{model_owner}/{model_name}/versions",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def delete(
        self,
        version_id: str,
        *,
        model_owner: str,
        model_name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete a model version and all associated predictions, including all output
        files.

        Model version deletion has some restrictions:

        - You can only delete versions from models you own.
        - You can only delete versions from private models.
        - You cannot delete a version if someone other than you has run predictions with
          it.
        - You cannot delete a version if it is being used as the base model for a fine
          tune/training.
        - You cannot delete a version if it has an associated deployment.
        - You cannot delete a version if another model version is overridden to use it.

        Example cURL request:

        ```command
        curl -s -X DELETE \\
          -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
          https://api.replicate.com/v1/models/replicate/hello-world/versions/5c7d5dc6dd8bf75c1acaa8565735e7986bc5b66206b55cca93cb72c9bf15ccaa
        ```

        The response will be an empty 202, indicating the deletion request has been
        accepted. It might take a few minutes to be processed.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_owner:
            raise ValueError(f"Expected a non-empty value for `model_owner` but received {model_owner!r}")
        if not model_name:
            raise ValueError(f"Expected a non-empty value for `model_name` but received {model_name!r}")
        if not version_id:
            raise ValueError(f"Expected a non-empty value for `version_id` but received {version_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/models/{model_owner}/{model_name}/versions/{version_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def create_training(
        self,
        version_id: str,
        *,
        model_owner: str,
        model_name: str,
        destination: str,
        input: object,
        webhook: str | NotGiven = NOT_GIVEN,
        webhook_events_filter: List[Literal["start", "output", "logs", "completed"]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SchemasTraining:
        """
        Start a new training of the model version you specify.

        Example request body:

        ```json
        {
          "destination": "{new_owner}/{new_name}",
          "input": {
            "train_data": "https://example.com/my-input-images.zip"
          },
          "webhook": "https://example.com/my-webhook"
        }
        ```

        Example cURL request:

        ```console
        curl -s -X POST \\
          -d '{"destination": "{new_owner}/{new_name}", "input": {"input_images": "https://example.com/my-input-images.zip"}}' \\
          -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
          -H 'Content-Type: application/json' \\
          https://api.replicate.com/v1/models/stability-ai/sdxl/versions/da77bc59ee60423279fd632efb4795ab731d9e3ca9705ef3341091fb989b7eaf/trainings
        ```

        The response will be the training object:

        ```json
        {
          "id": "zz4ibbonubfz7carwiefibzgga",
          "model": "stability-ai/sdxl",
          "version": "da77bc59ee60423279fd632efb4795ab731d9e3ca9705ef3341091fb989b7eaf",
          "input": {
            "input_images": "https://example.com/my-input-images.zip"
          },
          "logs": "",
          "error": null,
          "status": "starting",
          "created_at": "2023-09-08T16:32:56.990893084Z",
          "urls": {
            "cancel": "https://api.replicate.com/v1/predictions/zz4ibbonubfz7carwiefibzgga/cancel",
            "get": "https://api.replicate.com/v1/predictions/zz4ibbonubfz7carwiefibzgga"
          }
        }
        ```

        As models can take several minutes or more to train, the result will not be
        available immediately. To get the final result of the training you should either
        provide a `webhook` HTTPS URL for us to call when the results are ready, or poll
        the [get a training](#trainings.get) endpoint until it has finished.

        When a training completes, it creates a new
        [version](https://replicate.com/docs/how-does-replicate-work#terminology) of the
        model at the specified destination.

        To find some models to train on, check out the
        [trainable language models collection](https://replicate.com/collections/trainable-language-models).

        Args:
          destination: A string representing the desired model to push to in the format
              `{destination_model_owner}/{destination_model_name}`. This should be an existing
              model owned by the user or organization making the API request. If the
              destination is invalid, the server will return an appropriate 4XX response.

          input: An object containing inputs to the Cog model's `train()` function.

          webhook: An HTTPS URL for receiving a webhook when the training completes. The webhook
              will be a POST request where the request body is the same as the response body
              of the [get training](#trainings.get) operation. If there are network problems,
              we will retry the webhook a few times, so make sure it can be safely called more
              than once. Replicate will not follow redirects when sending webhook requests to
              your service, so be sure to specify a URL that will resolve without redirecting.

          webhook_events_filter: By default, we will send requests to your webhook URL whenever there are new
              outputs or the training has finished. You can change which events trigger
              webhook requests by specifying `webhook_events_filter` in the training request:

              - `start`: immediately on training start
              - `output`: each time a training generates an output (note that trainings can
                generate multiple outputs)
              - `logs`: each time log output is generated by a training
              - `completed`: when the training reaches a terminal state
                (succeeded/canceled/failed)

              For example, if you only wanted requests to be sent at the start and end of the
              training, you would provide:

              ```json
              {
                "destination": "my-organization/my-model",
                "input": {
                  "text": "Alice"
                },
                "webhook": "https://example.com/my-webhook",
                "webhook_events_filter": ["start", "completed"]
              }
              ```

              Requests for event types `output` and `logs` will be sent at most once every
              500ms. If you request `start` and `completed` webhooks, then they'll always be
              sent regardless of throttling.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_owner:
            raise ValueError(f"Expected a non-empty value for `model_owner` but received {model_owner!r}")
        if not model_name:
            raise ValueError(f"Expected a non-empty value for `model_name` but received {model_name!r}")
        if not version_id:
            raise ValueError(f"Expected a non-empty value for `version_id` but received {version_id!r}")
        return await self._post(
            f"/models/{model_owner}/{model_name}/versions/{version_id}/trainings",
            body=await async_maybe_transform(
                {
                    "destination": destination,
                    "input": input,
                    "webhook": webhook,
                    "webhook_events_filter": webhook_events_filter,
                },
                version_create_training_params.VersionCreateTrainingParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SchemasTraining,
        )


class VersionsResourceWithRawResponse:
    def __init__(self, versions: VersionsResource) -> None:
        self._versions = versions

        self.retrieve = to_raw_response_wrapper(
            versions.retrieve,
        )
        self.list = to_raw_response_wrapper(
            versions.list,
        )
        self.delete = to_raw_response_wrapper(
            versions.delete,
        )
        self.create_training = to_raw_response_wrapper(
            versions.create_training,
        )


class AsyncVersionsResourceWithRawResponse:
    def __init__(self, versions: AsyncVersionsResource) -> None:
        self._versions = versions

        self.retrieve = async_to_raw_response_wrapper(
            versions.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            versions.list,
        )
        self.delete = async_to_raw_response_wrapper(
            versions.delete,
        )
        self.create_training = async_to_raw_response_wrapper(
            versions.create_training,
        )


class VersionsResourceWithStreamingResponse:
    def __init__(self, versions: VersionsResource) -> None:
        self._versions = versions

        self.retrieve = to_streamed_response_wrapper(
            versions.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            versions.list,
        )
        self.delete = to_streamed_response_wrapper(
            versions.delete,
        )
        self.create_training = to_streamed_response_wrapper(
            versions.create_training,
        )


class AsyncVersionsResourceWithStreamingResponse:
    def __init__(self, versions: AsyncVersionsResource) -> None:
        self._versions = versions

        self.retrieve = async_to_streamed_response_wrapper(
            versions.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            versions.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            versions.delete,
        )
        self.create_training = async_to_streamed_response_wrapper(
            versions.create_training,
        )
