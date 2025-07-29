# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime

from .._models import BaseModel
from .cloud_zone import CloudZone

__all__ = ["ScheduleOption"]


class ScheduleOption(BaseModel):
    co2_intensity: float

    time: datetime

    zone: CloudZone
