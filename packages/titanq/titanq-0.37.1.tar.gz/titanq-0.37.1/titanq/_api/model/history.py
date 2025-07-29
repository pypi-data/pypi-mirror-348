# Copyright (c) 2025, InfinityQ Technology, Inc.

from datetime import datetime
from typing import List, Optional
import uuid
from pydantic import BaseModel, Field, RootModel, field_serializer


class ComputationHistoryRequest(BaseModel):
    id: Optional[uuid.UUID] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    @field_serializer("start_date", "end_date")
    def serialize_date(self, value: Optional[datetime]) -> Optional[str]:
        if value:
            return value.strftime("%Y-%m-%d")
        return None


class Status(BaseModel):
    status: str = Field(alias="Status")
    timestamp: datetime = Field(alias="TimeStamp")
    computation_id: uuid.UUID = Field(alias="ComputationID")
    note: str = Field(alias="Note")


class ComputationHistory(BaseModel):
    id: uuid.UUID
    account_id: uuid.UUID
    cost: int
    status: List[Status]


class ComputationHistoryResponse(RootModel):
    root: List[ComputationHistory]

    def __len__(self):
        return len(self.root)

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]