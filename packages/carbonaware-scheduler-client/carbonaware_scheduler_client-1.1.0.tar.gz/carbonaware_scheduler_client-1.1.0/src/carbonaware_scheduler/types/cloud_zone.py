# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["CloudZone"]


class CloudZone(BaseModel):
    provider: Literal["aws", "gcp", "azure"]

    region: Literal[
        "us-east-1",
        "us-west-1",
        "eu-central-1",
        "ap-southeast-2",
        "us-central1",
        "eastus",
        "eastus2",
        "southcentralus",
        "westus2",
        "westus3",
        "northeurope",
        "swedencentral",
        "uksouth",
        "westeurope",
        "centralus",
        "francecentral",
        "germanywestcentral",
        "italynorth",
        "norwayeast",
        "polandcentral",
        "eastus2euap",
        "eastusstg",
        "northcentralus",
        "westus",
        "centraluseuap",
        "westcentralus",
        "francesouth",
        "germanynorth",
        "norwaywest",
        "ukwest",
    ]
