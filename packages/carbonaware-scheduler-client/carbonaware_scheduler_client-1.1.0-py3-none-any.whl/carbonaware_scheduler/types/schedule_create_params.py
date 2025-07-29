# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable, Optional
from datetime import datetime
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo
from .cloud_zone_param import CloudZoneParam

__all__ = ["ScheduleCreateParams", "Window"]


class ScheduleCreateParams(TypedDict, total=False):
    duration: Required[str]

    windows: Required[Iterable[Window]]
    """List of time windows to schedule (start and end must be in the future)"""

    zones: Required[Iterable[CloudZoneParam]]

    num_options: Optional[int]


class Window(TypedDict, total=False):
    end: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    start: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]
