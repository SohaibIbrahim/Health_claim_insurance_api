# used to define the blueprint
from pydantic import BaseModel, validator
from datetime import datetime
from decimal import Decimal
from typing import Optional
from app.models.claim import ClaimStatus

class ClaimBase(BaseModel):
    patient_name: str
    diagnosis_code: str
    procedure_code: str
    claim_amount: Decimal
    
    @validator('claim_amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Claim amount must be positive')
        return v

class ClaimCreate(ClaimBase):
    pass

class ClaimUpdate(BaseModel):
    status: ClaimStatus

class Claim(ClaimBase):
    id: int
    status: ClaimStatus
    submitted_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class ClaimResponse(BaseModel):
    claims: list[Claim]
    total: int
    page: int
    per_page: int
    pages: int