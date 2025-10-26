"""Test login API"""
import requests
import json

# Login request
login_data = {
    "email": "test@example.com",
    "password": "password123"
}

print("Testing login API...")
print(f"URL: http://localhost:8000/api/auth/login")
print(f"Data: {json.dumps(login_data, indent=2)}")

response = requests.post(
    "http://localhost:8000/api/auth/login",
    json=login_data
)

print(f"\nStatus Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

if response.status_code == 200:
    print("\n=== Login successful! ===")
    token = response.json()["access_token"]
    print(f"Access Token: {token[:50]}...")

    # Test authenticated endpoint
    print("\n\nTesting authenticated endpoint...")
    headers = {
        "Authorization": f"Bearer {token}"
    }

    me_response = requests.get(
        "http://localhost:8000/api/auth/me",
        headers=headers
    )

    print(f"Status Code: {me_response.status_code}")
    print(f"User Info: {json.dumps(me_response.json(), indent=2)}")
else:
    print("\n=== Login failed ===")
