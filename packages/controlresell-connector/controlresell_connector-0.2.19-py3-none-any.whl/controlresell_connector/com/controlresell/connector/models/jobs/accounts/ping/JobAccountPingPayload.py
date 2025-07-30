from pydantic import BaseModel
from uuid import UUID

class JobAccountPingPayload(BaseModel):
    accountId: UUID
