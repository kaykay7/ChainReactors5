#!/usr/bin/env python3
"""
Test script to verify Composio is working and can pull Google Sheets data.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_composio_connection():
    """Test if Composio is properly configured."""
    print("🔍 Testing Composio Connection...")
    
    # Check environment variables
    api_key = os.getenv("COMPOSIO_API_KEY")
    user_id = os.getenv("COMPOSIO_USER_ID")
    
    if not api_key:
        print("❌ COMPOSIO_API_KEY not found in environment")
        return False
    
    if not user_id:
        print("❌ COMPOSIO_USER_ID not found in environment")
        return False
    
    print(f"✅ COMPOSIO_API_KEY: {api_key[:10]}...")
    print(f"✅ COMPOSIO_USER_ID: {user_id}")
    
    # Test Composio import
    try:
        from composio import Composio
        print("✅ Composio package imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Composio: {e}")
        print("💡 Install with: pip install composio")
        return False
    
    # Test Composio client initialization
    try:
        composio = Composio()
        print("✅ Composio client initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize Composio client: {e}")
        return False

def test_google_sheets_connection(sheet_id: str):
    """Test if we can connect to Google Sheets via Composio."""
    print(f"\n🔍 Testing Google Sheets Connection for Sheet ID: {sheet_id}")
    
    try:
        from composio import Composio
        
        composio = Composio()
        user_id = os.getenv("COMPOSIO_USER_ID", "default")
        
        # Test getting spreadsheet info
        print("📊 Testing GOOGLESHEETS_GET_SPREADSHEET_INFO...")
        result = composio.tools.execute(
            user_id=user_id,
            slug="GOOGLESHEETS_GET_SPREADSHEET_INFO",
            arguments={"spreadsheet_id": sheet_id}
        )
        
        if result and result.get("successful"):
            print("✅ Successfully connected to Google Sheets!")
            
            # Print spreadsheet info
            data = result.get("data", {}).get("response_data", {})
            title = data.get("properties", {}).get("title", "Unknown")
            sheets = data.get("sheets", [])
            
            print(f"📋 Spreadsheet Title: {title}")
            print(f"📊 Number of sheets: {len(sheets)}")
            
            for i, sheet in enumerate(sheets):
                sheet_name = sheet.get("properties", {}).get("title", f"Sheet {i+1}")
                print(f"   - Sheet {i+1}: {sheet_name}")
            
            return True
        else:
            print(f"❌ Failed to get spreadsheet info: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Google Sheets connection: {e}")
        return False

def main():
    """Main testing function."""
    print("🚀 Composio Testing Suite")
    print("=" * 50)
    
    # Test 1: Basic Composio connection
    if not test_composio_connection():
        print("\n❌ Composio connection failed. Please check your setup.")
        return
    
    print("\n✅ Composio connection successful!")
    
    # Test 2: Google Sheets connection (you'll need to provide a real sheet ID)
    sheet_id = input("\n📝 Enter a Google Sheet ID to test (or press Enter to skip): ").strip()
    
    if sheet_id:
        if test_google_sheets_connection(sheet_id):
            print("\n✅ Google Sheets connection successful!")
        else:
            print("\n❌ Google Sheets connection failed.")
    else:
        print("\n⏭️  Skipping Google Sheets tests.")
    
    print("\n" + "=" * 50)
    print("🏁 Testing complete!")

if __name__ == "__main__":
    main()
