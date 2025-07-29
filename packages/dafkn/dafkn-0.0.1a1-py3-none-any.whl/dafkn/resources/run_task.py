# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import run_task_execute_params
from .._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options

__all__ = ["RunTaskResource", "AsyncRunTaskResource"]


class RunTaskResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> RunTaskResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/BetaMorfaSys/MorfaSys#accessing-raw-response-data-eg-headers
        """
        return RunTaskResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RunTaskResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/BetaMorfaSys/MorfaSys#with_streaming_response
        """
        return RunTaskResourceWithStreamingResponse(self)

    def execute(
        self,
        *,
        payload: object | NotGiven = NOT_GIVEN,
        task: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Run a universal task or trigger via Zapier/n8n/custom endpoint

        Args:
          payload: Key-value pairs of input data needed by the task

          task: The name of the task to run (e.g. "send_email", "create_doc", "post_to_slack")

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/run-task",
            body=maybe_transform(
                {
                    "payload": payload,
                    "task": task,
                },
                run_task_execute_params.RunTaskExecuteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncRunTaskResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncRunTaskResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/BetaMorfaSys/MorfaSys#accessing-raw-response-data-eg-headers
        """
        return AsyncRunTaskResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRunTaskResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/BetaMorfaSys/MorfaSys#with_streaming_response
        """
        return AsyncRunTaskResourceWithStreamingResponse(self)

    async def execute(
        self,
        *,
        payload: object | NotGiven = NOT_GIVEN,
        task: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Run a universal task or trigger via Zapier/n8n/custom endpoint

        Args:
          payload: Key-value pairs of input data needed by the task

          task: The name of the task to run (e.g. "send_email", "create_doc", "post_to_slack")

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/run-task",
            body=await async_maybe_transform(
                {
                    "payload": payload,
                    "task": task,
                },
                run_task_execute_params.RunTaskExecuteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class RunTaskResourceWithRawResponse:
    def __init__(self, run_task: RunTaskResource) -> None:
        self._run_task = run_task

        self.execute = to_raw_response_wrapper(
            run_task.execute,
        )


class AsyncRunTaskResourceWithRawResponse:
    def __init__(self, run_task: AsyncRunTaskResource) -> None:
        self._run_task = run_task

        self.execute = async_to_raw_response_wrapper(
            run_task.execute,
        )


class RunTaskResourceWithStreamingResponse:
    def __init__(self, run_task: RunTaskResource) -> None:
        self._run_task = run_task

        self.execute = to_streamed_response_wrapper(
            run_task.execute,
        )


class AsyncRunTaskResourceWithStreamingResponse:
    def __init__(self, run_task: AsyncRunTaskResource) -> None:
        self._run_task = run_task

        self.execute = async_to_streamed_response_wrapper(
            run_task.execute,
        )
