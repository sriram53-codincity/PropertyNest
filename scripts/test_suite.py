import time
import os
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.database.connection import SessionLocal
from app.models.pg_models import UserRole, User

print("Starting API Test Suite...")

with TestClient(app) as client:
    print("\n--- 1. Authentication ---")
    email = f"test_{int(time.time())}@example.com"
    pwd = "password123"

    # Register
    res = client.post("/api/auth/register", json={
        "full_name": "Test User",
        "email": email,
        "password": pwd,
        "confirm_password": pwd
    })
    print("Register:", res.status_code, res.json())
    assert res.status_code == 200, "Failed to register"
    
    # Login
    res = client.post("/api/auth/login", json={
        "email": email,
        "password": pwd
    })
    print("Login:", res.status_code)
    assert res.status_code == 200, "Failed to login"
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    print("\n--- 2. Profile & Roles ---")
    res = client.get("/api/auth/me", headers=headers)
    print("Get Profile:", res.status_code, res.json())
    assert res.status_code == 200, "Failed to get profile"
    user_id = res.json()["id"]

    # Promote to ADMIN manually for testing
    db = SessionLocal()
    db.add(UserRole(user_id=user_id, role="ADMIN"))
    db.add(UserRole(user_id=user_id, role="SELLER"))
    db.commit()
    db.close()

    # Need new token for new roles
    res = client.post("/api/auth/login", json={"email": email, "password": pwd})
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    print("\n--- 3. Seller Requests ---")
    res = client.post("/api/seller-requests/", headers=headers, data={
        "full_name": "Test Seller",
        "phone": "1234567890",
        "address": "123 Main St",
        "property_title": "Test House",
        "property_address": "456 Test Ave",
        "property_type": "HOUSE",
        "monthly_rent": 1500.0,
        "doc_type": "DEED",
        "declaration_accepted": True
    }, files={
        "ownership_doc": ("test.pdf", b"dummy pdf content", "application/pdf"),
        "property_image": ("house.jpg", b"dummy image content", "image/jpeg")
    })
    print("Create Seller Request:", res.status_code, res.json())
    req_id = res.json()["request"]["id"]

    res = client.get("/api/seller-requests/", headers=headers)
    print("List Seller Requests:", res.status_code, len(res.json()))

    res = client.delete(f"/api/seller-requests/{req_id}", headers=headers)
    print("Delete Seller Request:", res.status_code, res.json())

    print("\n--- 4. Properties ---")
    res = client.post("/api/properties/", headers=headers, json={
        "title": "Beautiful Apartment",
        "city": "New York",
        "property_type": "APARTMENT",
        "bedrooms": 2,
        "bathrooms": 1,
        "monthly_rent": 2000.0,
        "description": "A very nice place",
        "amenities": ["WiFi", "Pool"]
    })
    print("Create Property:", res.status_code, res.json())
    prop_id = res.json()["property"]["id"]

    res = client.get("/api/properties/")
    print("List Properties:", res.status_code, len(res.json()))

    res = client.patch(f"/api/properties/{prop_id}", headers=headers, json={"status": "PUBLISHED"})
    print("Publish Property:", res.status_code)

    print("\n--- 5. Applications ---")
    res = client.post("/api/applications/", headers=headers, json={
        "property_id": str(prop_id),
        "full_name": "Test Applicant",
        "email": email,
        "phone": "0987654321",
        "date_of_birth": "1990-01-01",
        "marital_status": "SINGLE",
        "employment_type": "EMPLOYED",
        "current_address": "789 Old St",
        "move_in_date": "2024-01-01",
        "lease_duration": 12,
        "num_occupants": 1
    })
    print("Create Application:", res.status_code, res.json())
    app_id = res.json()["application"]["id"]

    res = client.patch(f"/api/applications/{app_id}/status", headers=headers, json={"status": "APPROVED"})
    print("Approve Application:", res.status_code)

    print("\n--- 6. Leases ---")
    res = client.post("/api/leases/", headers=headers, json={
        "application_id": str(app_id)
    })
    print("Create Lease:", res.status_code, res.json())
    lease_id = res.json()["lease"]["id"]

    res = client.get("/api/leases/me", headers=headers)
    print("List Leases:", res.status_code, len(res.json()))

    print("\n--- 7. Maintenance ---")
    res = client.post("/api/maintenance/", headers=headers, json={
        "lease_id": str(lease_id),
        "title": "Leaking Pipe",
        "category": "PLUMBING",
        "priority": "HIGH",
        "description": "The kitchen sink is leaking"
    })
    print("Create Maintenance:", res.status_code, res.json())
    maint_id = res.json()["request"]["id"]

    res = client.delete(f"/api/maintenance/{maint_id}", headers=headers)
    print("Delete Maintenance:", res.status_code, res.json())

    print("\n--- 8. Appointments ---")
    res = client.post("/api/appointments/", headers=headers, json={
        "full_name": "John Doe",
        "email": "john@test.com",
        "phone": "1231231234",
        "purpose": "PROPERTY_TOUR",
        "preferred_date": "2024-02-01",
        "preferred_time": "10:00 AM"
    })
    print("Book Appointment:", res.status_code, res.json())
    appt_id = res.json()["appointment"]["id"]

    res = client.delete(f"/api/appointments/{appt_id}", headers=headers)
    print("Delete Appointment:", res.status_code, res.json())

    print("\n--- 9. Cleanup ---")
    res = client.delete(f"/api/properties/{prop_id}", headers=headers)
    print("Delete Property:", res.status_code, res.json())

    print("\n--- ALL TESTS COMPLETED ---")
