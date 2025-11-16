"""
COGNIX AI - Quick Test Script
Tests the backend API without needing the frontend
"""

import asyncio
import httpx
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"


async def test_health():
    """Test health endpoint"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/health")
        print(f"✅ Health check: {response.json()}")


async def test_register_and_login():
    """Test user registration and login"""
    async with httpx.AsyncClient() as client:
        # Register new user
        register_data = {
            "email": f"test_{datetime.now().timestamp()}@cognix.ai",
            "password": "TestPassword123!",
            "full_name": "Test User"
        }
        
        response = await client.post(f"{BASE_URL}/auth/register", json=register_data)
        
        if response.status_code == 200:
            print(f"✅ User registered: {response.json()['user']['email']}")
        else:
            print(f"⚠️  Registration failed: {response.text}")
        
        # Login
        login_data = {
            "username": register_data["email"],
            "password": register_data["password"]
        }
        
        response = await client.post(
            f"{BASE_URL}/auth/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if response.status_code == 200:
            token_data = response.json()
            print(f"✅ Login successful: Token acquired")
            return token_data["access_token"]
        else:
            print(f"❌ Login failed: {response.text}")
            return None


async def test_domains(token: str):
    """Test domains endpoint"""
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {token}"}
        
        response = await client.get(f"{BASE_URL}/domains", headers=headers)
        
        if response.status_code == 200:
            domains = response.json()
            print(f"✅ Found {len(domains)} domains:")
            for domain in domains:
                print(f"   - {domain['name']}")
            return domains[0]['id']  # Return first domain ID
        else:
            print(f"❌ Domains fetch failed: {response.text}")
            return None


async def test_chat(token: str, domain: str):
    """Test chat endpoint"""
    async with httpx.AsyncClient(timeout=60.0) as client:
        headers = {"Authorization": f"Bearer {token}"}
        
        chat_request = {
            "message": "Show me the top 5 customers by revenue",
            "domain": domain
        }
        
        print(f"\n💬 Sending chat message: {chat_request['message']}")
        print(f"🎯 Domain: {domain}")
        print("⏳ Processing (this may take 10-20 seconds)...\n")
        
        response = await client.post(
            f"{BASE_URL}/chat",
            json=chat_request,
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Chat response received!")
            print(f"\n📨 Message: {result['message'][:200]}...")
            
            if result.get('agent_logs'):
                print(f"\n🤖 Agent Activity:")
                for log in result['agent_logs']:
                    print(f"   • {log['agent']}: {log['action'][:80]}")
            
            if result.get('metadata'):
                print(f"\n📊 Metadata:")
                metadata = result['metadata']
                if 'data' in metadata:
                    print(f"   - Data rows: {len(metadata['data'])}")
                if 'insights' in metadata:
                    print(f"   - Insights: {len(metadata['insights'])}")
                if 'visualization' in metadata:
                    print(f"   - Visualization: {metadata['visualization'].get('type', 'N/A')}")
        else:
            print(f"❌ Chat failed: {response.text}")


async def main():
    print("=" * 60)
    print("🚀 COGNIX AI - Backend API Test")
    print("=" * 60)
    print()
    
    try:
        # Test 1: Health check
        print("1️⃣  Testing health endpoint...")
        await test_health()
        print()
        
        # Test 2: Register and login
        print("2️⃣  Testing authentication...")
        token = await test_register_and_login()
        if not token:
            print("❌ Cannot proceed without authentication")
            return
        print()
        
        # Test 3: Get domains
        print("3️⃣  Testing domains...")
        domain = await test_domains(token)
        if not domain:
            print("❌ Cannot proceed without domain")
            return
        print()
        
        # Test 4: Chat with AI agents
        print("4️⃣  Testing chat with AI agents...")
        await test_chat(token, domain)
        print()
        
        print("=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("\n⚠️  Make sure the FastAPI server is running:")
    print("   cd backend && uvicorn main:app --reload\n")
    
    input("Press Enter to start tests...")
    
    asyncio.run(main())
