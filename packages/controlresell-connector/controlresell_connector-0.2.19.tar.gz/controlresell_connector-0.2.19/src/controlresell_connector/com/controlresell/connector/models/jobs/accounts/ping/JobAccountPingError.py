from pydantic import BaseModel
from uuid import UUID

class JobAccountPingError(BaseModel):
    accountId: UUID
