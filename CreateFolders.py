from Google import Create_Service

client_secret_file = 'client_secret_file.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(client_secret_file, API_NAME, API_VERSION, SCOPES)

files = ['Test1', 'Test2', 'Test3']
for file in files:
    file_metadata = {
        'name': file,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    file = service.files().create(body=file_metadata, fields='id').execute()
    print('Folder ID: %s' % file.get('id'))