from flask import Flask, request, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import openai

app = Flask(__name__)

SERVICE_ACCOUNT_FILE = 'service_account.json'
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/documents'
]

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/', methods=['POST'])
def save_doc_to_drive():
    data = request.get_json()
    doc_title = data.get('title')
    doc_content = data.get('content')

    try:
        docs_service = build('docs', 'v1', credentials=creds)
        drive_service = build('drive', 'v3', credentials=creds)

        # Create the doc
        doc = docs_service.documents().create(body={"title": doc_title}).execute()
        doc_id = doc.get('documentId')

        # Write content to the doc
        docs_service.documents().batchUpdate(
            documentId=doc_id,
            body={
                'requests': [{
                    'insertText': {
                        'location': {'index': 1},
                        'text': doc_content
                    }
                }]
            }
        ).execute()

        user_email = data.get('share_with')  # make sure to send this in your request JSON
        if user_email:
            permission = {
                'type': 'user',
                'role': 'writer',
                'emailAddress': user_email
            }
            drive_service.permissions().create(
            fileId=doc_id,
            body=permission,
            sendNotificationEmail=True
            ).execute()

        # Retrieve file metadata
        file = drive_service.files().get(fileId=doc_id, fields='id, webViewLink').execute()

        return jsonify({'message': 'Document created and saved.', 'link': file['webViewLink']}), 200

    except HttpError as e:
        return jsonify({'error': f'Google API error: {e}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def generate_gpt_edit():
    doc_id = doc.get('documentId')
    docs_service = build('docs', 'v1', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)

    # Read current doc content
    doc = docs_service.documents().get(documentId=doc_id).execute()
    content_blocks = doc.get('body', {}).get('content', [])
    full_text = ""

    for block in content_blocks:
        if 'paragraph' in block:
            for elem in block['paragraph'].get('elements', []):
                full_text += elem.get('textRun', {}).get('content', '')

    # Send to GPT
    prompt = f"In Section 5 of the following content, turn the bullet points into full paragraphs. Do not change anything else. Content:\n\n{full_text}"
    gpt_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    generated_text = gpt_response['choices'][0]['message']['content'].strip()

    # Insert at end
    end_index = content_blocks[-1]['endIndex'] if content_blocks else 1
    docs_service.documents().batchUpdate(
        documentId=doc_id,
        body={
            'requests': [{
                'insertText': {
                    'location': {'index': end_index - 1},
                    'text': f"\n\nGenerated Content:\n{generated_text}\n"
                }
            }]
        }
    ).execute()

    # Return updated doc link
    file = drive_service.files().get(fileId=doc_id, fields='id, webViewLink').execute()
    return file['webViewLink']

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)