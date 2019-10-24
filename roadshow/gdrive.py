from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import io
from googleapiclient.http import MediaIoBaseDownload
import time
from string import ascii_uppercase

class gdrive:
    def __init__(
        self,
        credential_file='credentials.json',
        SCOPES=['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets.readonly'],
        download_dir = 'datasets/roadshow/download',
        input_dir = 'datasets/roadshow/testA',
        output_dir = 'datasets/roadshow/results'):

        self.sleepTime = 1
        self.credential_file = credential_file
        self.SCOPES = SCOPES
        self.LETTERS = [letter for index, letter in enumerate(ascii_uppercase, start=1)]
        self.download_dir = download_dir
        self.output_dir = output_dir

        self.creds = self.getCreds()
        self.drive = self.getDrive()
        self.sheets = self.getSheets()
        print('gdrive init')

    def getCreds(self):
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
                while True:
                    try:
                        flow = InstalledAppFlow.from_client_secrets_file(
                            self.credential_file, self.SCOPES)
                        creds = flow.run_local_server(port=0)
                        break
                    except:
                        print('Retrying to get credentials')
                        time.sleep(self.sleepTime)
                        
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return creds

    def getDrive(self):
        return build('drive', 'v3', credentials=self.creds)

    def getSheets(self):
        return build('sheets', 'v4', credentials=self.creds)

    def createRange(self, start_row, columns):
        return 'A' + str(start_row) + ':' + self.LETTERS[columns-1]

    def getData(self, file_id, start_row, columns):
        sheet = self.sheets.spreadsheets()
        range = self.createRange(start_row, columns)

        result = sheet.values().get(spreadsheetId=file_id, range=range).execute().get('values', [])
        print(result)
        return start_row + len(result), result

    def printSheets(self, file_id, ranges):
        # Call the Sheets API
        sheet = self.sheets.spreadsheets()
        result = sheet.values().get(spreadsheetId=file_id,range=ranges).execute()
        print(result)
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            print('Name, Major:')
            for row in values:
                # Print columns A and E, which correspond to indices 0 and 4.
                print('%s, %s, %s, %s' % (row[0], row[1], row[2], row[3]))

    def listFiles(self):
        # Call the Drive v3 API
        results = self.drive.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))

    def upload(filename):
        pass

    def download(self, file_id):
        while True:
            try:
                name = self.drive.files().get(fileId=file_id).execute().get('name')
                request = self.drive.files().get_media(fileId=file_id)
                downloaded = io.BytesIO()
                downloader = MediaIoBaseDownload(downloaded, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    #print('Percent downloaded', int(100 * status.progress()))
                downloaded.seek(0)
                with open(os.path.join(self.download_dir, name), 'wb') as file:
                    file.write(downloaded.read())
                return name
            except:
                print('An error occurred while downloading file, retrying...')
                time.sleep(self.sleepTime)

    def poll(self, file_id):
        response = self.drive.changes().getStartPageToken().execute()
        start_page_token = response.get('startPageToken')
        print('Start token: %s' % start_page_token)

        while True:
            page_token = start_page_token
            while page_token is not None:
                response = self.drive.changes().list(pageToken=page_token,
                                                        spaces='drive').execute()
                for x in response.get('changes'):
                    if x.get('fileId') == file_id:
                        print('new form content')
                        return True
                if 'newStartPageToken' in response:
                    # Last page, save this token for the next polling interval
                    start_page_token = response.get('newStartPageToken')
                page_token = response.get('nextPageToken')
