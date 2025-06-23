import pytest

def test_create_claim(client, auth_headers):
    claim_data = {
        "patient_name": "John Doe",
        "diagnosis_code": "A01",
        "procedure_code": "P001",
        "claim_amount": 1500.00
    }
    
    response = client.post("/claims", json=claim_data, headers=auth_headers)
    assert response.status_code == 201
    
    data = response.json()
    assert data["patient_name"] == "John Doe"
    assert data["status"] == "PENDING"

def test_get_claims_with_filters(client, auth_headers):
    # First create some claims
    claims_data = [
        {"patient_name": "John Doe", "diagnosis_code": "A01", "procedure_code": "P001", "claim_amount": 1500.00},
        {"patient_name": "Jane Smith", "diagnosis_code": "B02", "procedure_code": "P002", "claim_amount": 2000.00}
    ]
    
    for claim in claims_data:
        client.post("/claims", json=claim, headers=auth_headers)
    
    # Test filtering
    response = client.get("/claims?diagnosis_code=A01", headers=auth_headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["total"] == 1
    assert data["claims"][0]["diagnosis_code"] == "A01"