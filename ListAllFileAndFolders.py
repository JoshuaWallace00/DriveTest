from Google import Create_Service
import pandas as pd

client_secret_file = 'client_secret_file.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(client_secret_file, API_NAME, API_VERSION, SCOPES)

folder_id = '1bPI-1ZnfWCCSPOgOu1g7I_R6PERcGmrU'

def list_files_and_folders(service):
    query = ""  # Empty query retrieves all files and folders
    results = service.files().list(q=query, pageSize=1000, fields="files(id, name, mimeType)").execute()
    items = results.get('files', [])
    next_page_token = results.get('nextPageToken')
    while next_page_token:
        results = service.files().list(q=query, pageSize=1000, pageToken=next_page_token, fields="files(id, name, mimeType)").execute()
        items.extend(results.get('files', []))
        next_page_token = results.get('nextPageToken')

    df = pd.DataFrame(items)
    print(df['name'])

list_files_and_folders(service)

