# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.training_list_response import TrainingListResponse
from ..types.models.schemas_training import SchemasTraining

__all__ = ["TrainingsResource", "AsyncTrainingsResource"]


class TrainingsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TrainingsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mihairu0511/stainlessTest#accessing-raw-response-data-eg-headers
        """
        return TrainingsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TrainingsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mihairu0511/stainlessTest#with_streaming_response
        """
        return TrainingsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        training_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SchemasTraining:
        """
        Get the current state of a training.

        Example cURL request:

        ```console
        curl -s \\
          -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
          https://api.replicate.com/v1/trainings/zz4ibbonubfz7carwiefibzgga
        ```

        The response will be the training object:

        ```json
        {
          "completed_at": "2023-09-08T16:41:19.826523Z",
          "created_at": "2023-09-08T16:32:57.018467Z",
          "error": null,
          "id": "zz4ibbonubfz7carwiefibzgga",
          "input": {
            "input_images": "https://example.com/my-input-images.zip"
          },
          "logs": "...",
          "metrics": {
            "predict_time": 502.713876
          },
          "output": {
            "version": "...",
            "weights": "..."
          },
          "started_at": "2023-09-08T16:32:57.112647Z",
          "status": "succeeded",
          "urls": {
            "get": "https://api.replicate.com/v1/trainings/zz4ibbonubfz7carwiefibzgga",
            "cancel": "https://api.replicate.com/v1/trainings/zz4ibbonubfz7carwiefibzgga/cancel"
          },
          "model": "stability-ai/sdxl",
          "version": "da77bc59ee60423279fd632efb4795ab731d9e3ca9705ef3341091fb989b7eaf"
        }
        ```

        `status` will be one of:

        - `starting`: the training is starting up. If this status lasts longer than a
          few seconds, then it's typically because a new worker is being started to run
          the training.
        - `processing`: the `train()` method of the model is currently running.
        - `succeeded`: the training completed successfully.
        - `failed`: the training encountered an error during processing.
        - `canceled`: the training was canceled by its creator.

        In the case of success, `output` will be an object containing the output of the
        model. Any files will be represented as HTTPS URLs. You'll need to pass the
        `Authorization` header to request them.

        In the case of failure, `error` will contain the error encountered during the
        training.

        Terminated trainings (with a status of `succeeded`, `failed`, or `canceled`)
        will include a `metrics` object with a `predict_time` property showing the
        amount of CPU or GPU time, in seconds, that the training used while running. It
        won't include time waiting for the training to start.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not training_id:
            raise ValueError(f"Expected a non-empty value for `training_id` but received {training_id!r}")
        return self._get(
            f"/trainings/{training_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SchemasTraining,
        )

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TrainingListResponse:
        """
        Get a paginated list of all trainings created by the user or organization
        associated with the provided API token.

        This will include trainings created from the API and the website. It will return
        100 records per page.

        Example cURL request:

        ```console
        curl -s \\
          -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
          https://api.replicate.com/v1/trainings
        ```

        The response will be a paginated JSON array of training objects, sorted with the
        most recent training first:

        ```json
        {
          "next": null,
          "previous": null,
          "results": [
            {
              "completed_at": "2023-09-08T16:41:19.826523Z",
              "created_at": "2023-09-08T16:32:57.018467Z",
              "error": null,
              "id": "zz4ibbonubfz7carwiefibzgga",
              "input": {
                "input_images": "https://example.com/my-input-images.zip"
              },
              "metrics": {
                "predict_time": 502.713876
              },
              "output": {
                "version": "...",
                "weights": "..."
              },
              "started_at": "2023-09-08T16:32:57.112647Z",
              "source": "api",
              "status": "succeeded",
              "urls": {
                "get": "https://api.replicate.com/v1/trainings/zz4ibbonubfz7carwiefibzgga",
                "cancel": "https://api.replicate.com/v1/trainings/zz4ibbonubfz7carwiefibzgga/cancel"
              },
              "model": "stability-ai/sdxl",
              "version": "da77bc59ee60423279fd632efb4795ab731d9e3ca9705ef3341091fb989b7eaf"
            }
          ]
        }
        ```

        `id` will be the unique ID of the training.

        `source` will indicate how the training was created. Possible values are `web`
        or `api`.

        `status` will be the status of the training. Refer to
        [get a single training](#trainings.get) for possible values.

        `urls` will be a convenience object that can be used to construct new API
        requests for the given training.

        `version` will be the unique ID of model version used to create the training.
        """
        return self._get(
            "/trainings",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TrainingListResponse,
        )

    def cancel(
        self,
        training_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SchemasTraining:
        """
        Cancel a training

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not training_id:
            raise ValueError(f"Expected a non-empty value for `training_id` but received {training_id!r}")
        return self._post(
            f"/trainings/{training_id}/cancel",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SchemasTraining,
        )


class AsyncTrainingsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTrainingsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mihairu0511/stainlessTest#accessing-raw-response-data-eg-headers
        """
        return AsyncTrainingsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTrainingsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mihairu0511/stainlessTest#with_streaming_response
        """
        return AsyncTrainingsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        training_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SchemasTraining:
        """
        Get the current state of a training.

        Example cURL request:

        ```console
        curl -s \\
          -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
          https://api.replicate.com/v1/trainings/zz4ibbonubfz7carwiefibzgga
        ```

        The response will be the training object:

        ```json
        {
          "completed_at": "2023-09-08T16:41:19.826523Z",
          "created_at": "2023-09-08T16:32:57.018467Z",
          "error": null,
          "id": "zz4ibbonubfz7carwiefibzgga",
          "input": {
            "input_images": "https://example.com/my-input-images.zip"
          },
          "logs": "...",
          "metrics": {
            "predict_time": 502.713876
          },
          "output": {
            "version": "...",
            "weights": "..."
          },
          "started_at": "2023-09-08T16:32:57.112647Z",
          "status": "succeeded",
          "urls": {
            "get": "https://api.replicate.com/v1/trainings/zz4ibbonubfz7carwiefibzgga",
            "cancel": "https://api.replicate.com/v1/trainings/zz4ibbonubfz7carwiefibzgga/cancel"
          },
          "model": "stability-ai/sdxl",
          "version": "da77bc59ee60423279fd632efb4795ab731d9e3ca9705ef3341091fb989b7eaf"
        }
        ```

        `status` will be one of:

        - `starting`: the training is starting up. If this status lasts longer than a
          few seconds, then it's typically because a new worker is being started to run
          the training.
        - `processing`: the `train()` method of the model is currently running.
        - `succeeded`: the training completed successfully.
        - `failed`: the training encountered an error during processing.
        - `canceled`: the training was canceled by its creator.

        In the case of success, `output` will be an object containing the output of the
        model. Any files will be represented as HTTPS URLs. You'll need to pass the
        `Authorization` header to request them.

        In the case of failure, `error` will contain the error encountered during the
        training.

        Terminated trainings (with a status of `succeeded`, `failed`, or `canceled`)
        will include a `metrics` object with a `predict_time` property showing the
        amount of CPU or GPU time, in seconds, that the training used while running. It
        won't include time waiting for the training to start.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not training_id:
            raise ValueError(f"Expected a non-empty value for `training_id` but received {training_id!r}")
        return await self._get(
            f"/trainings/{training_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SchemasTraining,
        )

    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TrainingListResponse:
        """
        Get a paginated list of all trainings created by the user or organization
        associated with the provided API token.

        This will include trainings created from the API and the website. It will return
        100 records per page.

        Example cURL request:

        ```console
        curl -s \\
          -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
          https://api.replicate.com/v1/trainings
        ```

        The response will be a paginated JSON array of training objects, sorted with the
        most recent training first:

        ```json
        {
          "next": null,
          "previous": null,
          "results": [
            {
              "completed_at": "2023-09-08T16:41:19.826523Z",
              "created_at": "2023-09-08T16:32:57.018467Z",
              "error": null,
              "id": "zz4ibbonubfz7carwiefibzgga",
              "input": {
                "input_images": "https://example.com/my-input-images.zip"
              },
              "metrics": {
                "predict_time": 502.713876
              },
              "output": {
                "version": "...",
                "weights": "..."
              },
              "started_at": "2023-09-08T16:32:57.112647Z",
              "source": "api",
              "status": "succeeded",
              "urls": {
                "get": "https://api.replicate.com/v1/trainings/zz4ibbonubfz7carwiefibzgga",
                "cancel": "https://api.replicate.com/v1/trainings/zz4ibbonubfz7carwiefibzgga/cancel"
              },
              "model": "stability-ai/sdxl",
              "version": "da77bc59ee60423279fd632efb4795ab731d9e3ca9705ef3341091fb989b7eaf"
            }
          ]
        }
        ```

        `id` will be the unique ID of the training.

        `source` will indicate how the training was created. Possible values are `web`
        or `api`.

        `status` will be the status of the training. Refer to
        [get a single training](#trainings.get) for possible values.

        `urls` will be a convenience object that can be used to construct new API
        requests for the given training.

        `version` will be the unique ID of model version used to create the training.
        """
        return await self._get(
            "/trainings",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TrainingListResponse,
        )

    async def cancel(
        self,
        training_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SchemasTraining:
        """
        Cancel a training

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not training_id:
            raise ValueError(f"Expected a non-empty value for `training_id` but received {training_id!r}")
        return await self._post(
            f"/trainings/{training_id}/cancel",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SchemasTraining,
        )


class TrainingsResourceWithRawResponse:
    def __init__(self, trainings: TrainingsResource) -> None:
        self._trainings = trainings

        self.retrieve = to_raw_response_wrapper(
            trainings.retrieve,
        )
        self.list = to_raw_response_wrapper(
            trainings.list,
        )
        self.cancel = to_raw_response_wrapper(
            trainings.cancel,
        )


class AsyncTrainingsResourceWithRawResponse:
    def __init__(self, trainings: AsyncTrainingsResource) -> None:
        self._trainings = trainings

        self.retrieve = async_to_raw_response_wrapper(
            trainings.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            trainings.list,
        )
        self.cancel = async_to_raw_response_wrapper(
            trainings.cancel,
        )


class TrainingsResourceWithStreamingResponse:
    def __init__(self, trainings: TrainingsResource) -> None:
        self._trainings = trainings

        self.retrieve = to_streamed_response_wrapper(
            trainings.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            trainings.list,
        )
        self.cancel = to_streamed_response_wrapper(
            trainings.cancel,
        )


class AsyncTrainingsResourceWithStreamingResponse:
    def __init__(self, trainings: AsyncTrainingsResource) -> None:
        self._trainings = trainings

        self.retrieve = async_to_streamed_response_wrapper(
            trainings.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            trainings.list,
        )
        self.cancel = async_to_streamed_response_wrapper(
            trainings.cancel,
        )
