# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx

from ..types import deployment_create_params, deployment_update_params, deployment_create_prediction_params
from .._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from .._utils import maybe_transform, strip_not_given, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.deployment_response import DeploymentResponse
from ..types.prediction_response import PredictionResponse
from ..types.deployment_list_response import DeploymentListResponse

__all__ = ["DeploymentsResource", "AsyncDeploymentsResource"]


class DeploymentsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DeploymentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mihairu0511/stainlessTest#accessing-raw-response-data-eg-headers
        """
        return DeploymentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DeploymentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mihairu0511/stainlessTest#with_streaming_response
        """
        return DeploymentsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        hardware: str,
        max_instances: int,
        min_instances: int,
        model: str,
        name: str,
        version: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DeploymentResponse:
        """
        Create a new deployment:

        Example cURL request:

        ```console
        curl -s \\
          -X POST \\
          -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
          -H "Content-Type: application/json" \\
          -d '{
                "name": "my-app-image-generator",
                "model": "stability-ai/sdxl",
                "version": "da77bc59ee60423279fd632efb4795ab731d9e3ca9705ef3341091fb989b7eaf",
                "hardware": "gpu-t4",
                "min_instances": 0,
                "max_instances": 3
              }' \\
          https://api.replicate.com/v1/deployments
        ```

        The response will be a JSON object describing the deployment:

        ```json
        {
          "owner": "acme",
          "name": "my-app-image-generator",
          "current_release": {
            "number": 1,
            "model": "stability-ai/sdxl",
            "version": "da77bc59ee60423279fd632efb4795ab731d9e3ca9705ef3341091fb989b7eaf",
            "created_at": "2024-02-15T16:32:57.018467Z",
            "created_by": {
              "type": "organization",
              "username": "acme",
              "name": "Acme Corp, Inc.",
              "avatar_url": "https://cdn.replicate.com/avatars/acme.png",
              "github_url": "https://github.com/acme"
            },
            "configuration": {
              "hardware": "gpu-t4",
              "min_instances": 1,
              "max_instances": 5
            }
          }
        }
        ```

        Args:
          hardware: The SKU for the hardware used to run the model. Possible values can be retrieved
              from the `hardware.list` endpoint.

          max_instances: The maximum number of instances for scaling.

          min_instances: The minimum number of instances for scaling.

          model: The full name of the model that you want to deploy e.g. stability-ai/sdxl.

          name: The name of the deployment.

          version: The 64-character string ID of the model version that you want to deploy.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/deployments",
            body=maybe_transform(
                {
                    "hardware": hardware,
                    "max_instances": max_instances,
                    "min_instances": min_instances,
                    "model": model,
                    "name": name,
                    "version": version,
                },
                deployment_create_params.DeploymentCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeploymentResponse,
        )

    def retrieve(
        self,
        deployment_name: str,
        *,
        deployment_owner: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DeploymentResponse:
        """
        Get information about a deployment by name including the current release.

        Example cURL request:

        ```console
        curl -s \\
          -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
          https://api.replicate.com/v1/deployments/replicate/my-app-image-generator
        ```

        The response will be a JSON object describing the deployment:

        ```json
        {
          "owner": "acme",
          "name": "my-app-image-generator",
          "current_release": {
            "number": 1,
            "model": "stability-ai/sdxl",
            "version": "da77bc59ee60423279fd632efb4795ab731d9e3ca9705ef3341091fb989b7eaf",
            "created_at": "2024-02-15T16:32:57.018467Z",
            "created_by": {
              "type": "organization",
              "username": "acme",
              "name": "Acme Corp, Inc.",
              "avatar_url": "https://cdn.replicate.com/avatars/acme.png",
              "github_url": "https://github.com/acme"
            },
            "configuration": {
              "hardware": "gpu-t4",
              "min_instances": 1,
              "max_instances": 5
            }
          }
        }
        ```

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_owner:
            raise ValueError(f"Expected a non-empty value for `deployment_owner` but received {deployment_owner!r}")
        if not deployment_name:
            raise ValueError(f"Expected a non-empty value for `deployment_name` but received {deployment_name!r}")
        return self._get(
            f"/deployments/{deployment_owner}/{deployment_name}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeploymentResponse,
        )

    def update(
        self,
        deployment_name: str,
        *,
        deployment_owner: str,
        hardware: str | NotGiven = NOT_GIVEN,
        max_instances: int | NotGiven = NOT_GIVEN,
        min_instances: int | NotGiven = NOT_GIVEN,
        version: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DeploymentResponse:
        """
        Update properties of an existing deployment, including hardware, min/max
        instances, and the deployment's underlying model
        [version](https://replicate.com/docs/how-does-replicate-work#versions).

        Example cURL request:

        ```console
        curl -s \\
          -X PATCH \\
          -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
          -H "Content-Type: application/json" \\
          -d '{"min_instances": 3, "max_instances": 10}' \\
          https://api.replicate.com/v1/deployments/acme/my-app-image-generator
        ```

        The response will be a JSON object describing the deployment:

        ```json
        {
          "owner": "acme",
          "name": "my-app-image-generator",
          "current_release": {
            "number": 2,
            "model": "stability-ai/sdxl",
            "version": "da77bc59ee60423279fd632efb4795ab731d9e3ca9705ef3341091fb989b7eaf",
            "created_at": "2024-02-15T16:32:57.018467Z",
            "created_by": {
              "type": "organization",
              "username": "acme",
              "name": "Acme Corp, Inc.",
              "avatar_url": "https://cdn.replicate.com/avatars/acme.png",
              "github_url": "https://github.com/acme"
            },
            "configuration": {
              "hardware": "gpu-t4",
              "min_instances": 3,
              "max_instances": 10
            }
          }
        }
        ```

        Updating any deployment properties will increment the `number` field of the
        `current_release`.

        Args:
          hardware: The SKU for the hardware used to run the model. Possible values can be retrieved
              from the `hardware.list` endpoint.

          max_instances: The maximum number of instances for scaling.

          min_instances: The minimum number of instances for scaling.

          version: The ID of the model version that you want to deploy

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_owner:
            raise ValueError(f"Expected a non-empty value for `deployment_owner` but received {deployment_owner!r}")
        if not deployment_name:
            raise ValueError(f"Expected a non-empty value for `deployment_name` but received {deployment_name!r}")
        return self._patch(
            f"/deployments/{deployment_owner}/{deployment_name}",
            body=maybe_transform(
                {
                    "hardware": hardware,
                    "max_instances": max_instances,
                    "min_instances": min_instances,
                    "version": version,
                },
                deployment_update_params.DeploymentUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeploymentResponse,
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
    ) -> DeploymentListResponse:
        """
        Get a list of deployments associated with the current account, including the
        latest release configuration for each deployment.

        Example cURL request:

        ```console
        curl -s \\
          -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
          https://api.replicate.com/v1/deployments
        ```

        The response will be a paginated JSON array of deployment objects, sorted with
        the most recent deployment first:

        ```json
        {
          "next": "http://api.replicate.com/v1/deployments?cursor=cD0yMDIzLTA2LTA2KzIzJTNBNDAlM0EwOC45NjMwMDAlMkIwMCUzQTAw",
          "previous": null,
          "results": [
            {
              "owner": "replicate",
              "name": "my-app-image-generator",
              "current_release": {
                "number": 1,
                "model": "stability-ai/sdxl",
                "version": "da77bc59ee60423279fd632efb4795ab731d9e3ca9705ef3341091fb989b7eaf",
                "created_at": "2024-02-15T16:32:57.018467Z",
                "created_by": {
                  "type": "organization",
                  "username": "acme",
                  "name": "Acme Corp, Inc.",
                  "avatar_url": "https://cdn.replicate.com/avatars/acme.png",
                  "github_url": "https://github.com/acme"
                },
                "configuration": {
                  "hardware": "gpu-t4",
                  "min_instances": 1,
                  "max_instances": 5
                }
              }
            }
          ]
        }
        ```
        """
        return self._get(
            "/deployments",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeploymentListResponse,
        )

    def delete(
        self,
        deployment_name: str,
        *,
        deployment_owner: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete a deployment

        Deployment deletion has some restrictions:

        - You can only delete deployments that have been offline and unused for at least
          15 minutes.

        Example cURL request:

        ```command
        curl -s -X DELETE \\
          -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
          https://api.replicate.com/v1/deployments/acme/my-app-image-generator
        ```

        The response will be an empty 204, indicating the deployment has been deleted.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_owner:
            raise ValueError(f"Expected a non-empty value for `deployment_owner` but received {deployment_owner!r}")
        if not deployment_name:
            raise ValueError(f"Expected a non-empty value for `deployment_name` but received {deployment_name!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/deployments/{deployment_owner}/{deployment_name}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def create_prediction(
        self,
        deployment_name: str,
        *,
        deployment_owner: str,
        input: object,
        stream: bool | NotGiven = NOT_GIVEN,
        webhook: str | NotGiven = NOT_GIVEN,
        webhook_events_filter: List[Literal["start", "output", "logs", "completed"]] | NotGiven = NOT_GIVEN,
        prefer: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PredictionResponse:
        """
        Create a prediction for the deployment and inputs you provide.

        Example cURL request:

        ```console
        curl -s -X POST -H 'Prefer: wait' \\
          -d '{"input": {"prompt": "A photo of a bear riding a bicycle over the moon"}}' \\
          -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
          -H 'Content-Type: application/json' \\
          https://api.replicate.com/v1/deployments/acme/my-app-image-generator/predictions
        ```

        The request will wait up to 60 seconds for the model to run. If this time is
        exceeded the prediction will be returned in a `"starting"` state and need to be
        retrieved using the `predictions.get` endpiont.

        For a complete overview of the `deployments.predictions.create` API check out
        our documentation on
        [creating a prediction](https://replicate.com/docs/topics/predictions/create-a-prediction)
        which covers a variety of use cases.

        Args:
          input: The model's input as a JSON object. The input schema depends on what model you
              are running. To see the available inputs, click the "API" tab on the model you
              are running or [get the model version](#models.versions.get) and look at its
              `openapi_schema` property. For example,
              [stability-ai/sdxl](https://replicate.com/stability-ai/sdxl) takes `prompt` as
              an input.

              Files should be passed as HTTP URLs or data URLs.

              Use an HTTP URL when:

              - you have a large file > 256kb
              - you want to be able to use the file multiple times
              - you want your prediction metadata to be associable with your input files

              Use a data URL when:

              - you have a small file <= 256kb
              - you don't want to upload and host the file somewhere
              - you don't need to use the file again (Replicate will not store it)

          stream: **This field is deprecated.**

              Request a URL to receive streaming output using
              [server-sent events (SSE)](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events).

              This field is no longer needed as the returned prediction will always have a
              `stream` entry in its `url` property if the model supports streaming.

          webhook: An HTTPS URL for receiving a webhook when the prediction has new output. The
              webhook will be a POST request where the request body is the same as the
              response body of the [get prediction](#predictions.get) operation. If there are
              network problems, we will retry the webhook a few times, so make sure it can be
              safely called more than once. Replicate will not follow redirects when sending
              webhook requests to your service, so be sure to specify a URL that will resolve
              without redirecting.

          webhook_events_filter: By default, we will send requests to your webhook URL whenever there are new
              outputs or the prediction has finished. You can change which events trigger
              webhook requests by specifying `webhook_events_filter` in the prediction
              request:

              - `start`: immediately on prediction start
              - `output`: each time a prediction generates an output (note that predictions
                can generate multiple outputs)
              - `logs`: each time log output is generated by a prediction
              - `completed`: when the prediction reaches a terminal state
                (succeeded/canceled/failed)

              For example, if you only wanted requests to be sent at the start and end of the
              prediction, you would provide:

              ```json
              {
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
        if not deployment_owner:
            raise ValueError(f"Expected a non-empty value for `deployment_owner` but received {deployment_owner!r}")
        if not deployment_name:
            raise ValueError(f"Expected a non-empty value for `deployment_name` but received {deployment_name!r}")
        extra_headers = {**strip_not_given({"Prefer": prefer}), **(extra_headers or {})}
        return self._post(
            f"/deployments/{deployment_owner}/{deployment_name}/predictions",
            body=maybe_transform(
                {
                    "input": input,
                    "stream": stream,
                    "webhook": webhook,
                    "webhook_events_filter": webhook_events_filter,
                },
                deployment_create_prediction_params.DeploymentCreatePredictionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PredictionResponse,
        )


class AsyncDeploymentsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDeploymentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mihairu0511/stainlessTest#accessing-raw-response-data-eg-headers
        """
        return AsyncDeploymentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDeploymentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mihairu0511/stainlessTest#with_streaming_response
        """
        return AsyncDeploymentsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        hardware: str,
        max_instances: int,
        min_instances: int,
        model: str,
        name: str,
        version: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DeploymentResponse:
        """
        Create a new deployment:

        Example cURL request:

        ```console
        curl -s \\
          -X POST \\
          -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
          -H "Content-Type: application/json" \\
          -d '{
                "name": "my-app-image-generator",
                "model": "stability-ai/sdxl",
                "version": "da77bc59ee60423279fd632efb4795ab731d9e3ca9705ef3341091fb989b7eaf",
                "hardware": "gpu-t4",
                "min_instances": 0,
                "max_instances": 3
              }' \\
          https://api.replicate.com/v1/deployments
        ```

        The response will be a JSON object describing the deployment:

        ```json
        {
          "owner": "acme",
          "name": "my-app-image-generator",
          "current_release": {
            "number": 1,
            "model": "stability-ai/sdxl",
            "version": "da77bc59ee60423279fd632efb4795ab731d9e3ca9705ef3341091fb989b7eaf",
            "created_at": "2024-02-15T16:32:57.018467Z",
            "created_by": {
              "type": "organization",
              "username": "acme",
              "name": "Acme Corp, Inc.",
              "avatar_url": "https://cdn.replicate.com/avatars/acme.png",
              "github_url": "https://github.com/acme"
            },
            "configuration": {
              "hardware": "gpu-t4",
              "min_instances": 1,
              "max_instances": 5
            }
          }
        }
        ```

        Args:
          hardware: The SKU for the hardware used to run the model. Possible values can be retrieved
              from the `hardware.list` endpoint.

          max_instances: The maximum number of instances for scaling.

          min_instances: The minimum number of instances for scaling.

          model: The full name of the model that you want to deploy e.g. stability-ai/sdxl.

          name: The name of the deployment.

          version: The 64-character string ID of the model version that you want to deploy.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/deployments",
            body=await async_maybe_transform(
                {
                    "hardware": hardware,
                    "max_instances": max_instances,
                    "min_instances": min_instances,
                    "model": model,
                    "name": name,
                    "version": version,
                },
                deployment_create_params.DeploymentCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeploymentResponse,
        )

    async def retrieve(
        self,
        deployment_name: str,
        *,
        deployment_owner: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DeploymentResponse:
        """
        Get information about a deployment by name including the current release.

        Example cURL request:

        ```console
        curl -s \\
          -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
          https://api.replicate.com/v1/deployments/replicate/my-app-image-generator
        ```

        The response will be a JSON object describing the deployment:

        ```json
        {
          "owner": "acme",
          "name": "my-app-image-generator",
          "current_release": {
            "number": 1,
            "model": "stability-ai/sdxl",
            "version": "da77bc59ee60423279fd632efb4795ab731d9e3ca9705ef3341091fb989b7eaf",
            "created_at": "2024-02-15T16:32:57.018467Z",
            "created_by": {
              "type": "organization",
              "username": "acme",
              "name": "Acme Corp, Inc.",
              "avatar_url": "https://cdn.replicate.com/avatars/acme.png",
              "github_url": "https://github.com/acme"
            },
            "configuration": {
              "hardware": "gpu-t4",
              "min_instances": 1,
              "max_instances": 5
            }
          }
        }
        ```

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_owner:
            raise ValueError(f"Expected a non-empty value for `deployment_owner` but received {deployment_owner!r}")
        if not deployment_name:
            raise ValueError(f"Expected a non-empty value for `deployment_name` but received {deployment_name!r}")
        return await self._get(
            f"/deployments/{deployment_owner}/{deployment_name}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeploymentResponse,
        )

    async def update(
        self,
        deployment_name: str,
        *,
        deployment_owner: str,
        hardware: str | NotGiven = NOT_GIVEN,
        max_instances: int | NotGiven = NOT_GIVEN,
        min_instances: int | NotGiven = NOT_GIVEN,
        version: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DeploymentResponse:
        """
        Update properties of an existing deployment, including hardware, min/max
        instances, and the deployment's underlying model
        [version](https://replicate.com/docs/how-does-replicate-work#versions).

        Example cURL request:

        ```console
        curl -s \\
          -X PATCH \\
          -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
          -H "Content-Type: application/json" \\
          -d '{"min_instances": 3, "max_instances": 10}' \\
          https://api.replicate.com/v1/deployments/acme/my-app-image-generator
        ```

        The response will be a JSON object describing the deployment:

        ```json
        {
          "owner": "acme",
          "name": "my-app-image-generator",
          "current_release": {
            "number": 2,
            "model": "stability-ai/sdxl",
            "version": "da77bc59ee60423279fd632efb4795ab731d9e3ca9705ef3341091fb989b7eaf",
            "created_at": "2024-02-15T16:32:57.018467Z",
            "created_by": {
              "type": "organization",
              "username": "acme",
              "name": "Acme Corp, Inc.",
              "avatar_url": "https://cdn.replicate.com/avatars/acme.png",
              "github_url": "https://github.com/acme"
            },
            "configuration": {
              "hardware": "gpu-t4",
              "min_instances": 3,
              "max_instances": 10
            }
          }
        }
        ```

        Updating any deployment properties will increment the `number` field of the
        `current_release`.

        Args:
          hardware: The SKU for the hardware used to run the model. Possible values can be retrieved
              from the `hardware.list` endpoint.

          max_instances: The maximum number of instances for scaling.

          min_instances: The minimum number of instances for scaling.

          version: The ID of the model version that you want to deploy

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_owner:
            raise ValueError(f"Expected a non-empty value for `deployment_owner` but received {deployment_owner!r}")
        if not deployment_name:
            raise ValueError(f"Expected a non-empty value for `deployment_name` but received {deployment_name!r}")
        return await self._patch(
            f"/deployments/{deployment_owner}/{deployment_name}",
            body=await async_maybe_transform(
                {
                    "hardware": hardware,
                    "max_instances": max_instances,
                    "min_instances": min_instances,
                    "version": version,
                },
                deployment_update_params.DeploymentUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeploymentResponse,
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
    ) -> DeploymentListResponse:
        """
        Get a list of deployments associated with the current account, including the
        latest release configuration for each deployment.

        Example cURL request:

        ```console
        curl -s \\
          -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
          https://api.replicate.com/v1/deployments
        ```

        The response will be a paginated JSON array of deployment objects, sorted with
        the most recent deployment first:

        ```json
        {
          "next": "http://api.replicate.com/v1/deployments?cursor=cD0yMDIzLTA2LTA2KzIzJTNBNDAlM0EwOC45NjMwMDAlMkIwMCUzQTAw",
          "previous": null,
          "results": [
            {
              "owner": "replicate",
              "name": "my-app-image-generator",
              "current_release": {
                "number": 1,
                "model": "stability-ai/sdxl",
                "version": "da77bc59ee60423279fd632efb4795ab731d9e3ca9705ef3341091fb989b7eaf",
                "created_at": "2024-02-15T16:32:57.018467Z",
                "created_by": {
                  "type": "organization",
                  "username": "acme",
                  "name": "Acme Corp, Inc.",
                  "avatar_url": "https://cdn.replicate.com/avatars/acme.png",
                  "github_url": "https://github.com/acme"
                },
                "configuration": {
                  "hardware": "gpu-t4",
                  "min_instances": 1,
                  "max_instances": 5
                }
              }
            }
          ]
        }
        ```
        """
        return await self._get(
            "/deployments",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DeploymentListResponse,
        )

    async def delete(
        self,
        deployment_name: str,
        *,
        deployment_owner: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete a deployment

        Deployment deletion has some restrictions:

        - You can only delete deployments that have been offline and unused for at least
          15 minutes.

        Example cURL request:

        ```command
        curl -s -X DELETE \\
          -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
          https://api.replicate.com/v1/deployments/acme/my-app-image-generator
        ```

        The response will be an empty 204, indicating the deployment has been deleted.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_owner:
            raise ValueError(f"Expected a non-empty value for `deployment_owner` but received {deployment_owner!r}")
        if not deployment_name:
            raise ValueError(f"Expected a non-empty value for `deployment_name` but received {deployment_name!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/deployments/{deployment_owner}/{deployment_name}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def create_prediction(
        self,
        deployment_name: str,
        *,
        deployment_owner: str,
        input: object,
        stream: bool | NotGiven = NOT_GIVEN,
        webhook: str | NotGiven = NOT_GIVEN,
        webhook_events_filter: List[Literal["start", "output", "logs", "completed"]] | NotGiven = NOT_GIVEN,
        prefer: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PredictionResponse:
        """
        Create a prediction for the deployment and inputs you provide.

        Example cURL request:

        ```console
        curl -s -X POST -H 'Prefer: wait' \\
          -d '{"input": {"prompt": "A photo of a bear riding a bicycle over the moon"}}' \\
          -H "Authorization: Bearer $REPLICATE_API_TOKEN" \\
          -H 'Content-Type: application/json' \\
          https://api.replicate.com/v1/deployments/acme/my-app-image-generator/predictions
        ```

        The request will wait up to 60 seconds for the model to run. If this time is
        exceeded the prediction will be returned in a `"starting"` state and need to be
        retrieved using the `predictions.get` endpiont.

        For a complete overview of the `deployments.predictions.create` API check out
        our documentation on
        [creating a prediction](https://replicate.com/docs/topics/predictions/create-a-prediction)
        which covers a variety of use cases.

        Args:
          input: The model's input as a JSON object. The input schema depends on what model you
              are running. To see the available inputs, click the "API" tab on the model you
              are running or [get the model version](#models.versions.get) and look at its
              `openapi_schema` property. For example,
              [stability-ai/sdxl](https://replicate.com/stability-ai/sdxl) takes `prompt` as
              an input.

              Files should be passed as HTTP URLs or data URLs.

              Use an HTTP URL when:

              - you have a large file > 256kb
              - you want to be able to use the file multiple times
              - you want your prediction metadata to be associable with your input files

              Use a data URL when:

              - you have a small file <= 256kb
              - you don't want to upload and host the file somewhere
              - you don't need to use the file again (Replicate will not store it)

          stream: **This field is deprecated.**

              Request a URL to receive streaming output using
              [server-sent events (SSE)](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events).

              This field is no longer needed as the returned prediction will always have a
              `stream` entry in its `url` property if the model supports streaming.

          webhook: An HTTPS URL for receiving a webhook when the prediction has new output. The
              webhook will be a POST request where the request body is the same as the
              response body of the [get prediction](#predictions.get) operation. If there are
              network problems, we will retry the webhook a few times, so make sure it can be
              safely called more than once. Replicate will not follow redirects when sending
              webhook requests to your service, so be sure to specify a URL that will resolve
              without redirecting.

          webhook_events_filter: By default, we will send requests to your webhook URL whenever there are new
              outputs or the prediction has finished. You can change which events trigger
              webhook requests by specifying `webhook_events_filter` in the prediction
              request:

              - `start`: immediately on prediction start
              - `output`: each time a prediction generates an output (note that predictions
                can generate multiple outputs)
              - `logs`: each time log output is generated by a prediction
              - `completed`: when the prediction reaches a terminal state
                (succeeded/canceled/failed)

              For example, if you only wanted requests to be sent at the start and end of the
              prediction, you would provide:

              ```json
              {
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
        if not deployment_owner:
            raise ValueError(f"Expected a non-empty value for `deployment_owner` but received {deployment_owner!r}")
        if not deployment_name:
            raise ValueError(f"Expected a non-empty value for `deployment_name` but received {deployment_name!r}")
        extra_headers = {**strip_not_given({"Prefer": prefer}), **(extra_headers or {})}
        return await self._post(
            f"/deployments/{deployment_owner}/{deployment_name}/predictions",
            body=await async_maybe_transform(
                {
                    "input": input,
                    "stream": stream,
                    "webhook": webhook,
                    "webhook_events_filter": webhook_events_filter,
                },
                deployment_create_prediction_params.DeploymentCreatePredictionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PredictionResponse,
        )


class DeploymentsResourceWithRawResponse:
    def __init__(self, deployments: DeploymentsResource) -> None:
        self._deployments = deployments

        self.create = to_raw_response_wrapper(
            deployments.create,
        )
        self.retrieve = to_raw_response_wrapper(
            deployments.retrieve,
        )
        self.update = to_raw_response_wrapper(
            deployments.update,
        )
        self.list = to_raw_response_wrapper(
            deployments.list,
        )
        self.delete = to_raw_response_wrapper(
            deployments.delete,
        )
        self.create_prediction = to_raw_response_wrapper(
            deployments.create_prediction,
        )


class AsyncDeploymentsResourceWithRawResponse:
    def __init__(self, deployments: AsyncDeploymentsResource) -> None:
        self._deployments = deployments

        self.create = async_to_raw_response_wrapper(
            deployments.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            deployments.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            deployments.update,
        )
        self.list = async_to_raw_response_wrapper(
            deployments.list,
        )
        self.delete = async_to_raw_response_wrapper(
            deployments.delete,
        )
        self.create_prediction = async_to_raw_response_wrapper(
            deployments.create_prediction,
        )


class DeploymentsResourceWithStreamingResponse:
    def __init__(self, deployments: DeploymentsResource) -> None:
        self._deployments = deployments

        self.create = to_streamed_response_wrapper(
            deployments.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            deployments.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            deployments.update,
        )
        self.list = to_streamed_response_wrapper(
            deployments.list,
        )
        self.delete = to_streamed_response_wrapper(
            deployments.delete,
        )
        self.create_prediction = to_streamed_response_wrapper(
            deployments.create_prediction,
        )


class AsyncDeploymentsResourceWithStreamingResponse:
    def __init__(self, deployments: AsyncDeploymentsResource) -> None:
        self._deployments = deployments

        self.create = async_to_streamed_response_wrapper(
            deployments.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            deployments.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            deployments.update,
        )
        self.list = async_to_streamed_response_wrapper(
            deployments.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            deployments.delete,
        )
        self.create_prediction = async_to_streamed_response_wrapper(
            deployments.create_prediction,
        )
