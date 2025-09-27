#!/usr/bin/env python3
"""
Simple test to check if Composio is working.
"""

import os

def test_composio():
    """Test Composio connection and configuration."""
    print("🔍 Testing Composio Setup...")
    print("=" * 40)
    
    # Check environment variables
    api_key = os.getenv("COMPOSIO_API_KEY")
    user_id = os.getenv("COMPOSIO_USER_ID")
    
    print(f"COMPOSIO_API_KEY: {'✅ Found' if api_key else '❌ Missing'}")
    print(f"COMPOSIO_USER_ID: {'✅ Found' if user_id else '❌ Missing'}")
    
    if not api_key:
        print("\n❌ COMPOSIO_API_KEY not found!")
        print("💡 Add it to your .env file:")
        print("COMPOSIO_API_KEY=your_api_key_here")
        return False
    
    if not user_id:
        print("\n❌ COMPOSIO_USER_ID not found!")
        print("💡 Add it to your .env file:")
        print("COMPOSIO_USER_ID=your_user_id_here")
        return False
    
    # Test Composio import
    try:
        from composio import Composio
        print("✅ Composio package imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Composio: {e}")
        return False
    
    # Test Composio client
    try:
        composio = Composio()
        print("✅ Composio client initialized successfully")
        print("\n🎉 Composio is properly configured!")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize Composio client: {e}")
        return False

if __name__ == "__main__":
    test_composio()
