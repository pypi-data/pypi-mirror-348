# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .cloud_zone import CloudZone

__all__ = ["RegionListResponse"]


class RegionListResponse(BaseModel):
    regions: List[CloudZone]
