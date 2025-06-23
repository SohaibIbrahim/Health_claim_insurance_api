from fastapi import APIRouter, Depends, HTTPException, status, Query,Request
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.database import get_db
from app.models.claim import Claim, ClaimStatus
from app.models.user import User
from app.schemas.claim import ClaimCreate, ClaimUpdate, Claim as ClaimSchema, ClaimResponse
from app.core.dependencies import get_current_user

# Rate limiting setup
limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/claims", tags=["claims"])

@router.post("", response_model=ClaimSchema, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def create_claim(
    request: Request , # For rate limiting
    claim: ClaimCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_claim = Claim(**claim.dict())
    db.add(db_claim)
    db.commit()
    db.refresh(db_claim)
    return db_claim

@router.get("", response_model=ClaimResponse)
async def get_claims(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    status: Optional[ClaimStatus] = None,
    diagnosis_code: Optional[str] = None,
    procedure_code: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Claim)
    
    # Apply filters
    if status:
        query = query.filter(Claim.status == status)
    if diagnosis_code:
        query = query.filter(Claim.diagnosis_code == diagnosis_code)
    if procedure_code:
        query = query.filter(Claim.procedure_code == procedure_code)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    claims = query.offset((page - 1) * per_page).limit(per_page).all()
    
    return ClaimResponse(
        claims=claims,
        total=total,
        page=page,
        per_page=per_page,
        pages=(total + per_page - 1) // per_page
    )

@router.get("/{claim_id}", response_model=ClaimSchema)
async def get_claim(
    claim_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if not claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim not found"
        )
    return claim

@router.put("/{claim_id}", response_model=ClaimSchema)
async def update_claim(
    claim_id: int,
    claim_update: ClaimUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if not claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim not found"
        )
    
    claim.status = claim_update.status
    db.commit()
    db.refresh(claim)
    return claim

@router.delete("/{claim_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_claim(
    claim_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if not claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim not found"
        )
    
    db.delete(claim)
    db.commit()