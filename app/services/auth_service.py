from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload
from app.models.pg_models import User, UserRole
from app.auth import hash_password, verify_password, create_token
from app.schemas.auth_schema import RegisterBody, LoginBody

async def register_user(body: RegisterBody, db: AsyncSession):
    """
    Registers a new user in the system.

    Args:
        body (RegisterBody): The user registration details.
        db (AsyncSession): The database session.

    Raises:
        HTTPException 400: If passwords do not match or email is already registered.

    Returns:
        dict: A success message and the new user's ID.
    """
    if body.password != body.confirm_password:
        raise HTTPException(400, "Passwords do not match")

    result = await db.execute(select(User).filter(User.email == body.email))
    existing = result.scalars().first()
    if existing:
        raise HTTPException(400, "Email already registered")

    new_user = User(
        full_name=body.full_name,
        email=body.email,
        password=hash_password(body.password)
    )
    
    try:
        db.add(new_user)
        await db.flush()
        
        role = UserRole(user_id=new_user.id, role="TENANT")
        db.add(role)
        await db.commit()
    except Exception:
        await db.rollback()
        raise

    await db.refresh(new_user)
    return {"message": "Registered successfully", "user_id": str(new_user.id)}

async def login_user(body: LoginBody, db: AsyncSession):
    """
    Authenticates a user and returns a JWT token.

    Args:
        body (LoginBody): The user's login credentials.
        db (AsyncSession): The database session.

    Raises:
        HTTPException 401: If invalid email or password provided.

    Returns:
        dict: The access token, token type, and user roles.
    """
    result = await db.execute(select(User).options(selectinload(User.roles)).filter(User.email == body.email))
    user = result.scalars().first()

    if not user or not verify_password(body.password, user.password):
        raise HTTPException(401, "Invalid email or password")

    roles = [r.role for r in user.roles]

    token = create_token(str(user.id), roles)
    return {"access_token": token, "token_type": "bearer", "roles": roles}

async def get_current_user_profile(user_id: str, db: AsyncSession):
    """
    Retrieves the profile of the current authenticated user.

    Args:
        user_id (str): The ID of the user.
        db (AsyncSession): The database session.

    Raises:
        HTTPException 404: If the user is not found.

    Returns:
        dict: User profile information.
    """
    result = await db.execute(select(User).options(selectinload(User.roles)).filter(User.id == int(user_id)))
    user = result.scalars().first()

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

async def get_all_users_admin(db: AsyncSession):
    result = await db.execute(select(User).options(selectinload(User.roles)).order_by(desc(User.created_at)))
    users = result.scalars().all()
    out = []
    for user in users:
        roles = [r.role for r in user.roles]
        out.append({
            "id": str(user.id),
            "full_name": user.full_name,
            "email": user.email,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "roles": roles
        })
    return out

async def delete_user_admin(user_id: str, db: AsyncSession):
    result = await db.execute(select(User).options(selectinload(User.roles)).filter(User.id == int(user_id)))
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(404, "User not found")
    
    if any(r.role == "ADMIN" for r in user.roles):
        raise HTTPException(400, "Cannot delete an admin user")

    try:
        await db.delete(user)
        await db.commit()
    except Exception:
        await db.rollback()
        raise
        
    return {"message": "User deleted successfully"}
