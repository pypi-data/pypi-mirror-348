# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from carbonaware_scheduler import CarbonawareScheduler, AsyncCarbonawareScheduler
from carbonaware_scheduler.types import ScheduleCreateResponse
from carbonaware_scheduler._utils import parse_datetime

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSchedule:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: CarbonawareScheduler) -> None:
        schedule = client.schedule.create(
            duration="PT1H",
            windows=[
                {
                    "end": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "start": parse_datetime("2019-12-27T18:11:19.117Z"),
                }
            ],
            zones=[
                {
                    "provider": "aws",
                    "region": "us-east-1",
                }
            ],
        )
        assert_matches_type(ScheduleCreateResponse, schedule, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: CarbonawareScheduler) -> None:
        schedule = client.schedule.create(
            duration="PT1H",
            windows=[
                {
                    "end": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "start": parse_datetime("2019-12-27T18:11:19.117Z"),
                }
            ],
            zones=[
                {
                    "provider": "aws",
                    "region": "us-east-1",
                }
            ],
            num_options=0,
        )
        assert_matches_type(ScheduleCreateResponse, schedule, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: CarbonawareScheduler) -> None:
        response = client.schedule.with_raw_response.create(
            duration="PT1H",
            windows=[
                {
                    "end": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "start": parse_datetime("2019-12-27T18:11:19.117Z"),
                }
            ],
            zones=[
                {
                    "provider": "aws",
                    "region": "us-east-1",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        schedule = response.parse()
        assert_matches_type(ScheduleCreateResponse, schedule, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: CarbonawareScheduler) -> None:
        with client.schedule.with_streaming_response.create(
            duration="PT1H",
            windows=[
                {
                    "end": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "start": parse_datetime("2019-12-27T18:11:19.117Z"),
                }
            ],
            zones=[
                {
                    "provider": "aws",
                    "region": "us-east-1",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            schedule = response.parse()
            assert_matches_type(ScheduleCreateResponse, schedule, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSchedule:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncCarbonawareScheduler) -> None:
        schedule = await async_client.schedule.create(
            duration="PT1H",
            windows=[
                {
                    "end": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "start": parse_datetime("2019-12-27T18:11:19.117Z"),
                }
            ],
            zones=[
                {
                    "provider": "aws",
                    "region": "us-east-1",
                }
            ],
        )
        assert_matches_type(ScheduleCreateResponse, schedule, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncCarbonawareScheduler) -> None:
        schedule = await async_client.schedule.create(
            duration="PT1H",
            windows=[
                {
                    "end": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "start": parse_datetime("2019-12-27T18:11:19.117Z"),
                }
            ],
            zones=[
                {
                    "provider": "aws",
                    "region": "us-east-1",
                }
            ],
            num_options=0,
        )
        assert_matches_type(ScheduleCreateResponse, schedule, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncCarbonawareScheduler) -> None:
        response = await async_client.schedule.with_raw_response.create(
            duration="PT1H",
            windows=[
                {
                    "end": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "start": parse_datetime("2019-12-27T18:11:19.117Z"),
                }
            ],
            zones=[
                {
                    "provider": "aws",
                    "region": "us-east-1",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        schedule = await response.parse()
        assert_matches_type(ScheduleCreateResponse, schedule, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncCarbonawareScheduler) -> None:
        async with async_client.schedule.with_streaming_response.create(
            duration="PT1H",
            windows=[
                {
                    "end": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "start": parse_datetime("2019-12-27T18:11:19.117Z"),
                }
            ],
            zones=[
                {
                    "provider": "aws",
                    "region": "us-east-1",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            schedule = await response.parse()
            assert_matches_type(ScheduleCreateResponse, schedule, path=["response"])

        assert cast(Any, response.is_closed) is True
