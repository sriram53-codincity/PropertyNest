from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.pg_models import User, UserRole
from app.auth import hash_password, verify_password, create_token
from app.schemas.auth_schema import RegisterBody, LoginBody

def register_user(body: RegisterBody, db: Session):
    if body.password != body.confirm_password:
        raise HTTPException(400, "Passwords do not match")

    existing = db.query(User).filter(User.email == body.email).first()
    if existing:
        raise HTTPException(400, "Email already registered")

    new_user = User(
        full_name=body.full_name,
        email=body.email,
        password=hash_password(body.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    role = UserRole(user_id=new_user.id, role="BUYER")
    db.add(role)
    db.commit()

    return {"message": "Registered successfully", "user_id": str(new_user.id)}

def login_user(body: LoginBody, db: Session):
    user = db.query(User).filter(User.email == body.email).first()

    if not user or not verify_password(body.password, user.password):
        raise HTTPException(401, "Invalid email or password")

    roles = [r.role for r in user.roles]

    token = create_token(str(user.id), roles)
    return {"access_token": token, "token_type": "bearer", "roles": roles}

def get_current_user_profile(user_id: str, db: Session):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(404, "User not found")

    roles = [r.role for r in user.roles]

    return {
        "id": str(user.id),
        "full_name": user.full_name,
        "email": user.email,
        "is_active": user.is_active,
        "created_at": user.created_at,
        "roles": roles
    }
