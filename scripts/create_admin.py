from app.database.connection import SessionLocal
from app.models.pg_models import User, UserRole
from app.auth import hash_password

print("--- Create Admin User ---")
email = input("Enter Admin Email: ")
password = input("Enter Admin Password: ")

db = SessionLocal()

# 1. Create the user
admin = User(
    full_name="System Admin", 
    email=email, 
    password=hash_password(password), 
    is_active=True
)
db.add(admin)
db.commit()

# 2. Give them the ADMIN role
role = UserRole(user_id=admin.id, role="ADMIN")
db.add(role)
db.commit()

print(f"Success! {email} is now an ADMIN.")
db.close()
