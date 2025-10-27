"""Test user creation script"""
import asyncio
from src.services.auth_service import auth_service


async def create_test_user():
    """Create test user account"""
    try:
        user_data = {
            "email": "test@example.com",
            "password": "password123",
            "name": "Test User"
        }

        user = await auth_service.register_user(user_data)
        print("Test user created successfully!")
        print(f"Email: {user['email']}")
        print(f"Name: {user['name']}")
        print(f"Role: {user['role']}")

    except Exception as e:
        print(f"Failed to create user: {e}")


if __name__ == "__main__":
    asyncio.run(create_test_user())
