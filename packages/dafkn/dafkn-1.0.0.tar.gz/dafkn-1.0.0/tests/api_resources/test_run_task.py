# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from dafkn import Dafkn, AsyncDafkn

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestRunTask:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_execute(self, client: Dafkn) -> None:
        run_task = client.run_task.execute()
        assert run_task is None

    @pytest.mark.skip()
    @parametrize
    def test_method_execute_with_all_params(self, client: Dafkn) -> None:
        run_task = client.run_task.execute(
            payload={},
            task="task",
        )
        assert run_task is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_execute(self, client: Dafkn) -> None:
        response = client.run_task.with_raw_response.execute()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run_task = response.parse()
        assert run_task is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_execute(self, client: Dafkn) -> None:
        with client.run_task.with_streaming_response.execute() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            run_task = response.parse()
            assert run_task is None

        assert cast(Any, response.is_closed) is True


class TestAsyncRunTask:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_execute(self, async_client: AsyncDafkn) -> None:
        run_task = await async_client.run_task.execute()
        assert run_task is None

    @pytest.mark.skip()
    @parametrize
    async def test_method_execute_with_all_params(self, async_client: AsyncDafkn) -> None:
        run_task = await async_client.run_task.execute(
            payload={},
            task="task",
        )
        assert run_task is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_execute(self, async_client: AsyncDafkn) -> None:
        response = await async_client.run_task.with_raw_response.execute()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run_task = await response.parse()
        assert run_task is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_execute(self, async_client: AsyncDafkn) -> None:
        async with async_client.run_task.with_streaming_response.execute() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            run_task = await response.parse()
            assert run_task is None

        assert cast(Any, response.is_closed) is True
