import csv
import os
from datetime import datetime
from celery import current_app as celery_app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.claim import Claim, ClaimStatus
from app.core.config import settings

# Create separate DB session for Celery tasks
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@celery_app.task
def generate_claims_report():
    db = SessionLocal()
    try:
        claims = db.query(Claim).all()
        
        # Group by status and calculate totals
        report_data = {}
        for claim in claims:
            status = claim.status.value
            if status not in report_data:
                report_data[status] = {'count': 0, 'total_amount': 0}
            
            report_data[status]['count'] += 1
            report_data[status]['total_amount'] += float(claim.claim_amount)
        
        # Generate CSV
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"claims_report_{timestamp}.csv"
        os.makedirs('reports', exist_ok=True)
        filepath = f"reports/{filename}"
        
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Status', 'Count', 'Total Amount'])
            
            for status, data in report_data.items():
                writer.writerow([status, data['count'], data['total_amount']])
        
        return {'filename': filename, 'filepath': filepath}
    
    finally:
        db.close()