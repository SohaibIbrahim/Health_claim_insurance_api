from sqlalchemy import Column, Integer, String, Numeric, Enum, DateTime
from sqlalchemy.sql import func
from app.database import Base
import enum

class ClaimStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    DENIED = "DENIED"

class Claim(Base):
    __tablename__ = "claims"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String(100), nullable=False)
    diagnosis_code = Column(String(20), nullable=False, index=True)
    procedure_code = Column(String(20), nullable=False, index=True)
    claim_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum(ClaimStatus), default=ClaimStatus.PENDING, index=True)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())