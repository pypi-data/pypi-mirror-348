# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional

import httpx

from ..types import schedule_create_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
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
from ..types.cloud_zone_param import CloudZoneParam
from ..types.schedule_create_response import ScheduleCreateResponse

__all__ = ["ScheduleResource", "AsyncScheduleResource"]


class ScheduleResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ScheduleResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/carbon-aware/scheduler-client-python#accessing-raw-response-data-eg-headers
        """
        return ScheduleResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ScheduleResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/carbon-aware/scheduler-client-python#with_streaming_response
        """
        return ScheduleResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        duration: str,
        windows: Iterable[schedule_create_params.Window],
        zones: Iterable[CloudZoneParam],
        num_options: Optional[int] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ScheduleCreateResponse:
        """
        Schedule

        Args:
          windows: List of time windows to schedule (start and end must be in the future)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v0/schedule/",
            body=maybe_transform(
                {
                    "duration": duration,
                    "windows": windows,
                    "zones": zones,
                    "num_options": num_options,
                },
                schedule_create_params.ScheduleCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScheduleCreateResponse,
        )


class AsyncScheduleResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncScheduleResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/carbon-aware/scheduler-client-python#accessing-raw-response-data-eg-headers
        """
        return AsyncScheduleResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncScheduleResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/carbon-aware/scheduler-client-python#with_streaming_response
        """
        return AsyncScheduleResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        duration: str,
        windows: Iterable[schedule_create_params.Window],
        zones: Iterable[CloudZoneParam],
        num_options: Optional[int] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ScheduleCreateResponse:
        """
        Schedule

        Args:
          windows: List of time windows to schedule (start and end must be in the future)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v0/schedule/",
            body=await async_maybe_transform(
                {
                    "duration": duration,
                    "windows": windows,
                    "zones": zones,
                    "num_options": num_options,
                },
                schedule_create_params.ScheduleCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScheduleCreateResponse,
        )


class ScheduleResourceWithRawResponse:
    def __init__(self, schedule: ScheduleResource) -> None:
        self._schedule = schedule

        self.create = to_raw_response_wrapper(
            schedule.create,
        )


class AsyncScheduleResourceWithRawResponse:
    def __init__(self, schedule: AsyncScheduleResource) -> None:
        self._schedule = schedule

        self.create = async_to_raw_response_wrapper(
            schedule.create,
        )


class ScheduleResourceWithStreamingResponse:
    def __init__(self, schedule: ScheduleResource) -> None:
        self._schedule = schedule

        self.create = to_streamed_response_wrapper(
            schedule.create,
        )


class AsyncScheduleResourceWithStreamingResponse:
    def __init__(self, schedule: AsyncScheduleResource) -> None:
        self._schedule = schedule

        self.create = async_to_streamed_response_wrapper(
            schedule.create,
        )
