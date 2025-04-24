from Google import Create_Service
from googleapiclient.http import MediaFileUpload

client_secret_file = 'client_secret_file.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(client_secret_file, API_NAME, API_VERSION, SCOPES)

folder_id = '1bPI-1ZnfWCCSPOgOu1g7I_R6PERcGmrU'

# Can create function to detect file type and set mime type

file_names = ['/Users/joshwallace/Downloads/Joshua Wallace- CV.docx']
mime_types = ['application/vnd.openxmlformats-officedocument.wordprocessingml.document']

def upload_files(service, folder_id, file_names, mime_types):
    for file_name, mime_type in zip(file_names, mime_types):
        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }
        media = MediaFileUpload(file_name, mimetype=mime_type)
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f'File ID: {file.get("id")}')
        print(f'Uploaded {file_name} to folder {folder_id} with MIME type {mime_type}')

upload_files(service, folder_id, file_names, mime_types)
