#!/usr/bin/env python3
import subprocess
import sys
import os

# Install required libraries
print("Installing Google API libraries...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "google-auth-oauthlib", "google-auth-httplib2", "google-api-python-client"])

from google.auth.oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import webbrowser

SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']

try:
    # Start OAuth flow
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)

    # Create services
    docs_service = build('docs', 'v1', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)

    # Read the outline
    with open('WEBSITE_OUTLINE.md', 'r', encoding='utf-8') as f:
        content = f.read()

    # Create a new Google Doc
    body = {'title': 'All Hands on Deck - Website Outline (EDITABLE)'}
    doc = docs_service.documents().create(body=body).execute()
    doc_id = doc.get('documentId')
    doc_url = f"https://docs.google.com/document/d/{doc_id}/edit"

    # Add content to the doc
    requests_list = []
    requests_list.append({
        'insertText': {
            'text': content,
            'location': {'index': 1}
        }
    })

    docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': requests_list}).execute()

    print("✓ Google Doc created successfully!")
    print(f"✓ Document: All Hands on Deck - Website Outline (EDITABLE)")
    print(f"✓ URL: {doc_url}")
    print("\nOpening document in browser...")

    # Open in browser
    webbrowser.open(doc_url)

except FileNotFoundError:
    print("\n⚠️  Google credentials file not found.")
    print("\nTo set up Google Drive integration:")
    print("1. Go to: https://console.cloud.google.com/")
    print("2. Create a new project")
    print("3. Enable Google Docs API and Google Drive API")
    print("4. Create OAuth 2.0 credentials (Desktop app)")
    print("5. Download as JSON and save as 'credentials.json' in this directory")
    print("\nAlternatively, you can:")
    print("- Go to https://docs.google.com/document/create")
    print("- Title it: 'All Hands on Deck - Website Outline (EDITABLE)'")
    print("- Copy and paste content from WEBSITE_OUTLINE.md")

except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nManual alternative:")
    print("- Go to https://docs.google.com/document/create")
    print("- Title it: 'All Hands on Deck - Website Outline (EDITABLE)'")
    print("- Copy and paste content from WEBSITE_OUTLINE.md")
