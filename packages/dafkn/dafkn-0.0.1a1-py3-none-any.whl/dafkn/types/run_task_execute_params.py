# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["RunTaskExecuteParams"]


class RunTaskExecuteParams(TypedDict, total=False):
    payload: object
    """Key-value pairs of input data needed by the task"""

    task: str
    """The name of the task to run (e.g. "send_email", "create_doc", "post_to_slack")"""
