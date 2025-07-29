# Copyright (c) 2025, InfinityQ Technology, Inc.

from dataclasses import dataclass
from typing import Dict


@dataclass
class AwsCredentials:
    """
    AWSCredentials is a data class that stores the credentials required
    to authenticate and interact with Amazon Web Service (AWS).
    """
    access_key_id: str
    secret_access_key: str


@dataclass
class GcpCredentials:
    """
    GCPCredentials is a data class that stores the credentials required
    to authenticate and interact with Google Cloud Platform (GCP) services.
    """
    json_key: Dict[str, str]