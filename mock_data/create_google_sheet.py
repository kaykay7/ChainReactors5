#!/usr/bin/env python3
"""
Create a Google Sheet with mock supply chain data.

This script creates a Google Sheet with the mock supply chain data
that can be used with the Supply Chain Optimization Agent.
"""

import csv
import json
import os
from typing import List, Dict, Any
from pathlib import Path

# You'll need to install these packages:
# pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("❌ Google API packages not installed. Run:")
    print("pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    exit(1)

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def authenticate_google_sheets():
    """Authenticate with Google Sheets API."""
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds

def create_supply_chain_sheet():
    """Create a Google Sheet with supply chain data."""
    creds = authenticate_google_sheets()
    service = build('sheets', 'v4', credentials=creds)
    
    # Create a new spreadsheet
    spreadsheet_body = {
        'properties': {
            'title': 'Supply Chain Management Dashboard'
        }
    }
    
    try:
        spreadsheet = service.spreadsheets().create(body=spreadsheet_body).execute()
        spreadsheet_id = spreadsheet['spreadsheetId']
        print(f"✅ Created Google Sheet: {spreadsheet_id}")
        print(f"🔗 URL: https://docs.google.com/spreadsheets/d/{spreadsheet_id}")
        
        # Read the CSV data
        csv_file_path = Path(__file__).parent / "google_sheets_format.csv"
        if not csv_file_path.exists():
            print(f"❌ CSV file not found: {csv_file_path}")
            return None
        
        # Prepare data for Google Sheets
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
        
        # Update the sheet with data
        range_name = 'Sheet1!A1'
        body = {
            'values': data
        }
        
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()
        
        print(f"✅ Updated {result.get('updatedCells')} cells")
        
        # Format the sheet
        format_requests = [
            {
                "repeatCell": {
                    "range": {
                        "sheetId": 0,
                        "startRowIndex": 0,
                        "endRowIndex": 1
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": {
                                "red": 0.2,
                                "green": 0.4,
                                "blue": 0.8
                            },
                            "textFormat": {
                                "foregroundColor": {
                                    "red": 1.0,
                                    "green": 1.0,
                                    "blue": 1.0
                                },
                                "bold": True
                            }
                        }
                    },
                    "fields": "userEnteredFormat(backgroundColor,textFormat)"
                }
            }
        ]
        
        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={'requests': format_requests}
        ).execute()
        
        print("✅ Formatted header row")
        
        return spreadsheet_id
        
    except HttpError as error:
        print(f"❌ Google Sheets API error: {error}")
        return None

def main():
    """Main function to create Google Sheet."""
    print("🚀 Creating Google Sheet with supply chain data...")
    
    # Check if credentials file exists
    if not os.path.exists('credentials.json'):
        print("❌ credentials.json not found!")
        print("📝 To get credentials.json:")
        print("1. Go to https://console.developers.google.com/")
        print("2. Create a new project or select existing one")
        print("3. Enable Google Sheets API")
        print("4. Create credentials (OAuth 2.0 Client ID)")
        print("5. Download the JSON file and rename it to 'credentials.json'")
        print("6. Place it in the same directory as this script")
        return
    
    spreadsheet_id = create_supply_chain_sheet()
    
    if spreadsheet_id:
        print(f"\n🎉 Success! Your Google Sheet is ready:")
        print(f"📊 Sheet ID: {spreadsheet_id}")
        print(f"🔗 URL: https://docs.google.com/spreadsheets/d/{spreadsheet_id}")
        print(f"\n💡 You can now use this Sheet ID in your Supply Chain Optimization Agent!")
        
        # Save the sheet ID for easy reference
        with open('sheet_id.txt', 'w') as f:
            f.write(spreadsheet_id)
        print(f"💾 Sheet ID saved to: sheet_id.txt")
    else:
        print("❌ Failed to create Google Sheet")

if __name__ == "__main__":
    main()
