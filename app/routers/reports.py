from fastapi import APIRouter, Depends, HTTPException, status
from celery.result import AsyncResult
from app.models.user import User
from app.core.dependencies import get_current_user
from app.services.report_service import generate_claims_report

router = APIRouter(prefix="/claims", tags=["reports"])

@router.post("/report")
async def trigger_report_generation(current_user: User = Depends(get_current_user)):
    task = generate_claims_report.delay()
    return {"task_id": task.id, "status": "Task initiated"}

@router.get("/report/{task_id}")
async def get_report_status(
    task_id: str,
    current_user: User = Depends(get_current_user)
):
    task_result = AsyncResult(task_id)
    
    if task_result.state == 'PENDING':
        return {"task_id": task_id, "status": "Processing"}
    elif task_result.state == 'SUCCESS':
        result = task_result.result
        return {
            "task_id": task_id,
            "status": "Completed",
            "download_url": f"/download/{result['filename']}"
        }
    else:
        return {"task_id": task_id, "status": "Failed", "error": str(task_result.info)}