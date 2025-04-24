from Google import Create_Service

client_secret_file = 'client_secret_file.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(client_secret_file, API_NAME, API_VERSION, SCOPES)

source_folder_id = '1bPI-1ZnfWCCSPOgOu1g7I_R6PERcGmrU'
target_folder_id = '1T-wbx_OSvZCZRhmwiyVU7dyHbJ17Q8Zj'

def move_files(service, source_folder_id, target_folder_id):
    # Get the list of files in the source folder
    query = f"'{source_folder_id}' in parents"
    results = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    items = results.get('files', [])
    next_page_token = results.get('nextPageToken')
    while next_page_token:
        results = service.files().list(q=query, fields="files(id, name, mimeType)", pageToken=next_page_token).execute()
        items.extend(results.get('files', []))
        next_page_token = results.get('nextPageToken')

    if not items:
        print('No files found in the source folder.')
    else:
        for item in items:
            if item['mimeType'] != 'application/vnd.google-apps.folder':
                file_id = item['id']
                file_name = item['name']
                print(f'Moving file: {file_name} (ID: {file_id})')
                # Move the file to the target folder
                service.files().update(fileId=file_id, addParents=target_folder_id, removeParents=source_folder_id).execute()
                print(f'File {file_name} moved to target folder.')

# Call the function to move files
move_files(service, source_folder_id, target_folder_id)