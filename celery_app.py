from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "healthcare_claims",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["app.services.report_service"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)