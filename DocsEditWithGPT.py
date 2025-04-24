from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from Google import Create_Service
import os
from openai import OpenAI
from google.oauth2 import service_account
from googleapiclient.discovery import build

Docs_creds = 'Docs_creds.json'
API_NAME = 'docs'
API_VERSION = 'v1'
SCOPES = ['https://www.googleapis.com/auth/documents']

docs_service = Create_Service(Docs_creds, API_NAME, API_VERSION, SCOPES)

# Set your OpenAI API Key
client = OpenAI(api_key = "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")


# === READ GOOGLE DOC CONTENT ===
def read_document(doc_id):
    doc = docs_service.documents().get(documentId=doc_id).execute()
    content = doc.get('body').get('content')
    text = ''
    for element in content:
        if 'paragraph' in element:
            for p_elem in element['paragraph'].get('elements', []):
                text += p_elem.get('textRun', {}).get('content', '')
    return text.strip()

def edit_with_chatgpt(original_text, instruction="Make this text more concise."):
    prompt = f"Instruction: {instruction}\n\nText:\n{original_text}\n\nRewritten:"
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert writer and editor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# === REPLACE DOCUMENT CONTENT ===
def replace_text(doc_id, new_text):
    try:
        # Fetch the document
        doc = docs_service.documents().get(documentId=doc_id).execute()
        content = doc.get('body', {}).get('content', [])
        if not content:
            print("The document is empty.")
            return
        end_index = content[-1].get('endIndex', 1)

        # Adjust end_index to exclude the newline character
        if end_index > 1:
            end_index -= 1

        # Prepare requests
        requests = []
        if end_index > 1:
            requests.append({
                'deleteContentRange': {
                    'range': {
                        'startIndex': 1,
                        'endIndex': end_index
                    }
                }
            })
        requests.append({
            'insertText': {
                'location': {'index': 1},
                'text': new_text
            }
        })

        # Execute batch update
        docs_service.documents().batchUpdate(
            documentId=doc_id, body={'requests': requests}).execute()
        print("Document updated successfully.")
    except Exception as e:
        print(f"Error updating document: {e}")

# === FULL FLOW ===
def run_edit(doc_id, instruction):
    print("Reading document...")
    original = read_document(doc_id)
    print("Sending to ChatGPT...")
    edited = edit_with_chatgpt(original, instruction)
    print("Updating Google Doc...")
    replace_text(doc_id, edited)
    print("Done!")

# === USAGE ===
if __name__ == '__main__':
    document_id = "1QhWpSxSIjLmsB1Q123YF3APsofKNaPPFX5OeUC3KtIs"
    edit_instruction = "Present this text in full sentences and paragraphs with no bullet points."
    run_edit(document_id, edit_instruction)