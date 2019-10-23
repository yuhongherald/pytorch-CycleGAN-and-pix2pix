from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import io
from googleapiclient.http import MediaIoBaseDownload

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']
file_id = '1Ubi4-MJflgn5J_5erkd7sZLNJxFwk93aZtSruOEWBUo'

def getService():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    return service

def listFiles(service):
    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))

def download(service, file_id):
    request = service.files().export_media(fileId=file_id,
                                                 mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))

def poll(service):
    response = service.changes().getStartPageToken().execute()
    start_page_token = response.get('startPageToken')
    print('Start token: %s' % start_page_token)

    while True:
        page_token = start_page_token
        while page_token is not None:
            response = service.changes().list(pageToken=page_token,
                                                    spaces='drive').execute()
            print('new')
            for change in (change for change in response.get('changes') if change.get('fileId') == fileid):
                print('new form content')
                download(service, change.get('fileId'))
                name = change.get('name')

            if 'newStartPageToken' in response:
                # Last page, save this token for the next polling interval
                start_page_token = response.get('newStartPageToken')
            page_token = response.get('nextPageToken')


def main():
    service = getService()
    #listFiles(service)
    #poll(service)
    download(service, file_id)

if __name__ == '__main__':
    main()