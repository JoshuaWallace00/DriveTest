from Google import Create_Service
from googleapiclient.http import MediaIoBaseDownload
import os
import io

client_secret_file = 'client_secret_file.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(client_secret_file, API_NAME, API_VERSION, SCOPES)

file_ids = ['1PQ5X_HfnU_Bi5CGOrPT0O2KKXAgiWj52']
file_names = ['CV-Josh.docx']

for file_id, file_name in zip(file_ids, file_names):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    fh.seek(0)
    with open(file_name, 'wb') as f:
        f.write(fh.read())
        fh.close()
    print(f"Downloaded {file_name} successfully.")