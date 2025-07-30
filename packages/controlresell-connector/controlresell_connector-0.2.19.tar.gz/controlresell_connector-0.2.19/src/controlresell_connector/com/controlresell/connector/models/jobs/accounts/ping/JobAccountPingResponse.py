from pydantic import BaseModel
from uuid import UUID

class JobAccountPingResponse(BaseModel):
    accountId: UUID
