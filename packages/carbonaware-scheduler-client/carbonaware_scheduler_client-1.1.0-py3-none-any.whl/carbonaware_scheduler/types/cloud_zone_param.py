# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["CloudZoneParam"]


class CloudZoneParam(TypedDict, total=False):
    provider: Required[Literal["aws", "gcp", "azure"]]

    region: Required[
        Literal[
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
    ]
