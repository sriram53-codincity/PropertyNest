import sys
import os
import asyncio
from datetime import date, timedelta
from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, not_, delete
from app.database.connection import AsyncSessionLocal
from app.models.pg_models import User, UserRole, Property, Application, Lease, MaintenanceRequest, Appointment
from app.auth import hash_password

async def async_clean_and_seed():
    async with AsyncSessionLocal() as db:
        print("Finding all non-admin users...")
        
        # Get admin user IDs
        result = await db.execute(select(UserRole.user_id).filter(UserRole.role == 'ADMIN'))
        admin_ids = [row[0] for row in result.all()]
        
        if not admin_ids:
            admin_ids = [-1] # Prevent empty list in IN clause
            
        print("Deleting non-admin users...")
        result = await db.execute(select(User).filter(User.id.notin_(admin_ids)))
        non_admins = result.scalars().all()
        for u in non_admins:
            await db.delete(u)
        await db.commit()
        
        print("Seeding proper test data...")
        pwd = hash_password("password123")
        
        u1 = User(full_name="Alice Smith", email="alice@testdata.com", password=pwd)
        u2 = User(full_name="Bob Jones", email="bob@testdata.com", password=pwd)
        u3 = User(full_name="Charlie Brown", email="charlie@testdata.com", password=pwd)
        db.add_all([u1, u2, u3])
        await db.commit()
        
        db.add_all([
            UserRole(user_id=u1.id, role="BUYER"),
            UserRole(user_id=u2.id, role="SELLER"),
            UserRole(user_id=u2.id, role="BUYER"),
            UserRole(user_id=u3.id, role="SELLER")
        ])
        await db.commit()
        
        p1 = Property(owner_id=u2.id, title="Bandra Sea-link Villa", city="Mumbai", property_type="HOUSE", bedrooms=4, bathrooms=3, monthly_rent=50000, status="PUBLISHED", is_available=True)
        p2 = Property(owner_id=u2.id, title="Cozy Delhi Studio", city="Delhi", property_type="APARTMENT", bedrooms=1, bathrooms=1, monthly_rent=25000, status="PUBLISHED", is_available=True)
        p3 = Property(owner_id=u3.id, title="Modern Bangalore Condo", city="Bangalore", property_type="APARTMENT", bedrooms=2, bathrooms=2, monthly_rent=32000, status="PUBLISHED", is_available=True)
        p4 = Property(owner_id=u3.id, title="Pending Chennai House", city="Chennai", property_type="HOUSE", bedrooms=3, bathrooms=2, monthly_rent=21000, status="PENDING", is_available=True)
        db.add_all([p1, p2, p3, p4])
        await db.commit()
        
        app1 = Application(property_id=p1.id, applicant_id=u1.id, full_name="Alice Smith", email="alice@testdata.com", phone="1234567890", date_of_birth=date(1990, 1, 1), marital_status="SINGLE", employment_type="FULL_TIME", company_name="Tech Corp", monthly_income=12000, current_address="123 Old St", move_in_date=date.today() + timedelta(days=15), lease_duration=12, num_occupants=1, status="PENDING")
        app2 = Application(property_id=p2.id, applicant_id=u1.id, full_name="Alice Smith", email="alice@testdata.com", phone="1234567890", date_of_birth=date(1990, 1, 1), marital_status="SINGLE", employment_type="FULL_TIME", company_name="Tech Corp", monthly_income=12000, current_address="123 Old St", move_in_date=date.today() + timedelta(days=30), lease_duration=24, num_occupants=1, status="APPROVED")
        db.add_all([app1, app2])
        await db.commit()
        
        lease1 = Lease(property_id=p2.id, tenant_id=u1.id, owner_id=u2.id, application_id=app2.id, start_date=date.today() - timedelta(days=30), end_date=date.today() + timedelta(days=335), monthly_rent=2500, status="ACTIVE")
        db.add(lease1)
        await db.commit()
        
        m1 = MaintenanceRequest(lease_id=lease1.id, property_id=p2.id, tenant_id=u1.id, title="Leaking Faucet", category="PLUMBING", priority="MEDIUM", description="The kitchen sink is leaking heavily.", status="OPEN")
        db.add(m1)
        await db.commit()
        
        apt1 = Appointment(user_id=u1.id, property_id=p3.id, owner_id=u3.id, full_name="Alice Smith", email="alice@testdata.com", phone="1234567890", purpose="PROPERTY_TOUR", preferred_date=date.today() + timedelta(days=2), preferred_time="10:00 AM", status="PENDING")
        db.add(apt1)
        await db.commit()
        
        print("Done! Proper test data seeded.")
        print("Users created:")
        print("- alice@testdata.com")
        print("- bob@testdata.com")
        print("- charlie@testdata.com")
        print("Password: password123")

if __name__ == "__main__":
    asyncio.run(async_clean_and_seed())
