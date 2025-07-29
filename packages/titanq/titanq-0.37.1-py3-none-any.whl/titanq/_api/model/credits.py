# Copyright (c) 2025, InfinityQ Technology, Inc.

from datetime import datetime
from typing import List
from pydantic import BaseModel, RootModel

class CreditEntry(BaseModel):
    credits: int
    start_date: datetime
    expiration_date: datetime
    credits_used: int


class GetCreditsResponse(RootModel):
    root: List[CreditEntry]

    def __len__(self):
        return len(self.root)

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]