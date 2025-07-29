# Copyright (c) 2025, InfinityQ Technology, Inc.

"""
Function helpers related to the Titanq api key
"""

# the official environment variable that is used in official documentation
import os
from typing import Optional

from titanq import errors


TITANQ_API_KEY_ENV = "TITANQ_API_KEY"


def get_and_validate_api_key(api_key: Optional[str]) -> str:
    """
    Validate the TitanQ's api_key. If the api_key argument is None, will try to fetch it from
    the environment variables.

    :return: The api key is validated

    :raises: MissingTitanQApiKey or InvalidTitanqApiKey
    """
    api_key = api_key or os.getenv(TITANQ_API_KEY_ENV)

    if api_key is None:
        raise errors.MissingTitanqApiKey(
            "No API key is provided. You can set your API key in the Model, "
            + "or you can set the environment variable TITANQ_API_KEY")

    return api_key