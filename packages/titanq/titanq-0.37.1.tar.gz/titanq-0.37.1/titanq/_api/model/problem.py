# Copyright (c) 2025, InfinityQ Technology, Inc.

from datetime import datetime
from http import HTTPStatus
from pydantic import BaseModel
import uuid

from titanq import errors


class Problem(BaseModel):
    """
    Problem represents an RFC 7807/RFC 9457-compliant error response.
    It defines the standard structure for problem details in HTTP APIs form TitanQ.
    """
    status_code: int
    type: str
    title: str
    detail: str
    instance: str
    timestamp: datetime
    trace_id: uuid.UUID
    status_text:str

    def raise_(self) -> None:
        """Raise the appropriate error associated with this problem"""

        if self.status_code == HTTPStatus.BAD_REQUEST:
            raise errors.BadRequest(f"{self.detail}")
        elif self.status_code == HTTPStatus.PAYMENT_REQUIRED:
            raise errors.NotEnoughCreditsError()

        elif 400 <= self.status_code < 500:
            raise errors.ClientError(f"{self.detail}")

        elif self.status_code == HTTPStatus.NOT_IMPLEMENTED:
            raise errors.UnsolvableRequestError()

        elif 500 <= self.status_code < 600:
            raise errors.ServerError(f"{self.detail}")

        raise errors.UnexpectedServerResponseError(f'{self.status_code} {self.detail}')