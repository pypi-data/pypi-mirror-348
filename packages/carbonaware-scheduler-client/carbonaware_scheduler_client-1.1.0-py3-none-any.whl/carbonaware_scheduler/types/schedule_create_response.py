# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .schedule_option import ScheduleOption

__all__ = ["ScheduleCreateResponse", "CarbonSavings"]


class CarbonSavings(BaseModel):
    vs_median_case: float

    vs_naive_case: float

    vs_worst_case: float


class ScheduleCreateResponse(BaseModel):
    carbon_savings: CarbonSavings

    ideal: ScheduleOption

    median_case: ScheduleOption

    naive_case: ScheduleOption

    options: List[ScheduleOption]

    worst_case: ScheduleOption
