from fastapi import APIRouter , Depends , UploadFile , File
from typing import Annotated 
from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.services.contract_service import contract_service , ContractService
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.contract import ContractResponse , ContractListResponse

contract_router = APIRouter(
    prefix="/contracts",
    tags=['Contracts']
)

@contract_router.post('/upload')
def upload(
    db: Annotated[Session,Depends(get_db)],
    current_user: Annotated[User,Depends(get_current_user)],
    service: Annotated[ContractService,Depends(contract_service)],
    file: Annotated[UploadFile,File()]
) -> ContractResponse:
    return service.upload_contract(
        db=db,
        current_user=current_user,
        file=file
    )
    
@contract_router.get('',response_model=ContractListResponse)
def get_contracts(
    db: Annotated[Session,Depends(get_db)],
    current_user: Annotated[User,Depends(get_current_user)],
    service: Annotated[ContractService,Depends(contract_service)]
) -> ContractListResponse:
    contracts = service.get_user_contracts(
        db=db,
        current_user=current_user
    )
    return {
        "contracts": contracts
    }