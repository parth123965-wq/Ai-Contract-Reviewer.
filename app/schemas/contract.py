from pydantic import BaseModel , ConfigDict
from app.models.contract import ContractStatus
from datetime import datetime

class ContractResponse(BaseModel):
    id: int
    original_filename: str
    file_size: int
    content_type: str
    status: ContractStatus
    created_at: datetime
    model_config = ConfigDict(
        from_attributes=True
    )
    
class ContractListResponse(BaseModel):
    contracts: list[ContractResponse]