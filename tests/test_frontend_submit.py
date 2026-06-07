import asyncio
import httpx

async def test_submit():
    async with httpx.AsyncClient() as client:
        # First login to get token
        res = await client.post("http://localhost:8000/api/auth/login", json={
            "email": "mathimaran12345678@gmail.com",
            "password": "Password123" # guessing from previous contexts, or let's create a new user
        })
        
        # Actually let's just register a new one to be sure
        res = await client.post("http://localhost:8000/api/auth/register", json={
            "full_name": "Test Application User",
            "email": "testapp2@example.com",
            "password": "Password123",
            "confirm_password": "Password123"
        })
        print("Register res:", res.status_code, res.text)
        
        res = await client.post("http://localhost:8000/api/auth/login", json={
            "email": "testapp2@example.com",
            "password": "Password123"
        })
        print("Login res:", res.status_code, res.text)
        token = res.json().get("access_token")
        print("Token:", token)
        
        # Now submit application
        # Create a dummy gov_id file
        files = {'gov_id': ('gov_id.jpg', b'dummy content', 'image/jpeg')}
        data = {
            'property_id': '312',
            'full_name': 'Test User',
            'email': 'testapp@example.com',
            'phone': '1234567890',
            'date_of_birth': '1990-01-01',
            'marital_status': 'SINGLE',
            'employment_type': 'EMPLOYED',
            'current_address': '123 Test St',
            'move_in_date': '2026-07-01',
            'lease_duration': '12',
            'num_occupants': '1'
        }
        
        res = await client.post(
            "http://localhost:8000/api/applications/",
            data=data,
            files=files,
            headers={"Authorization": f"Bearer {token}"}
        )
        print("Status:", res.status_code)
        print("Response:", res.text)

if __name__ == "__main__":
    asyncio.run(test_submit())
