import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_user_success(client: AsyncClient):
    response = await client.post("/api/auth/register", json={
        "full_name": "Test User",
        "email": "test@example.com",
        "password": "Password123",
        "confirm_password": "Password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Registered successfully"
    assert "user_id" in data

@pytest.mark.asyncio
async def test_register_user_mismatch_passwords(client: AsyncClient):
    response = await client.post("/api/auth/register", json={
        "full_name": "Test User",
        "email": "test2@example.com",
        "password": "Password123",
        "confirm_password": "Password456"
    })
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_login_user_success(client: AsyncClient):
    # Register first
    await client.post("/api/auth/register", json={
        "full_name": "Login User",
        "email": "login@example.com",
        "password": "Password123",
        "confirm_password": "Password123"
    })
    
    # Login
    response = await client.post("/api/auth/login", json={
        "email": "login@example.com",
        "password": "Password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "roles" in data

@pytest.mark.asyncio
async def test_login_user_invalid(client: AsyncClient):
    response = await client.post("/api/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "wrong"
    })
    assert response.status_code == 401
