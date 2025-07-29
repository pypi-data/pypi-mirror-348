# Copyright (c) 2024, InfinityQ Technology, Inc.

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional

from titanq._api.client import Client
from titanq import __title__ as titanq_title, __version__ as titanq_version
from titanq._util.api_key import get_and_validate_api_key

"""
Functions to query information about credits for a specific account.
"""

@dataclass
class CreditDetails():
    credits: int
    start_date: datetime
    expiration_date: datetime
    credits_used: int


@dataclass
class CreditsSummary():
    """
    The summary of credits information returned by the backend on credits request.

    Attributes
    ----------
    available_credits
        A list of `CreditDetails` objects representing credits that are still valid.
    total_available_credits
        The total amount of available credits.
    upcoming_credits
        A list of `CreditDetails` objects representing credits that have not yet started.
        This can be `None` if there are no upcoming credits.
    """
    available_credits: List[CreditDetails]
    total_available_credits: int
    upcoming_credits: Optional[List[CreditDetails]]


def get_credits_summary(api_key: str = None, base_server_url: str = "https://titanq.infinityq.io") -> CreditsSummary:
    """
    Query the amount of remaining credits and summarize available and upcoming credits.

    Parameters
    ----------
    api_key
        TitanQ API key to access the service.
        If not set, it will use the environment variable ``TITANQ_API_KEY``
    base_server_url
        TitanQ API server url, default set to ``https://titanq.infinityq.io``.

    Returns
    -------
    CreditsSummary
        An object containing the list of available credits, the total available credits,
        and the list of upcoming credits (if any).

    Raises
    ------
    MissingTitanqApiKey
        If no API key is set and is also not set as an environment variable
    """
    api_key = get_and_validate_api_key(api_key)
    client = Client(base_server_url, api_key, titanq_title, titanq_version)
    response = client.get_credits()

    upcoming_credits = []
    available_credits = []
    total_available_credits = 0

    now = datetime.now(timezone.utc)
    for credit_details in response.body:
        if credit_details.start_date > now:
            upcoming_credits.append(credit_details)
            continue
        if credit_details.expiration_date > now:
            available_credits.append(credit_details)
            total_available_credits += (credit_details.credits - credit_details.credits_used)

    return CreditsSummary(
        available_credits=available_credits,
        total_available_credits=total_available_credits,
        upcoming_credits=upcoming_credits if upcoming_credits else None
    )