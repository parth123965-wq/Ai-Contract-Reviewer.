from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional
from app.models.contract import Contract
from datetime import datetime , timezone

class ContractRepository:
    
    def create_contract(
        self,
        db: Session,
        contract: Contract
    ) -> Contract:
        db.add(contract)
        db.commit()
        db.refresh(contract)
        return contract
    
    def get_contract_by_id(
        self,
        db: Session,
        contract_id: int
    ) -> Optional[Contract]:
        statement = select(Contract).where(
            Contract.id == contract_id
        )
        return db.execute(statement=statement).scalar_one_or_none()
    
    def get_user_contracts(
        self,
        db: Session,
        user_id: int
    ) -> list[Contract]:
        statement = select(Contract).where(
            Contract.user_id == user_id, 
            Contract.is_deleted.is_(False)
        )
        return db.execute(statement=statement).scalars().all()
    
    def update_contract(
        self,
        db: Session,
        contract: Contract
    ) -> Contract:
        db.commit()
        db.refresh(contract)
        return contract
    
    def soft_delete_contract(
        self,
        db: Session,
        contract: Contract
    ) -> Contract:
        contract.is_deleted = True
        contract.deleted_at = datetime.now(timezone.utc)
        return self.update_contract(
            db=db,
            contract=contract
        )