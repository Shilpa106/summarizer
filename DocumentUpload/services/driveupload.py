from __future__ import print_function

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from oauth2client.service_account import ServiceAccountCredentials

from django.conf import settings
from apiclient.http import MediaFileUpload, MediaIoBaseUpload
import io
import os



# SCOPE for Authentication URI
SCOPES = settings.SCOPES
json_keyfile_path = settings.GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE

PERMISSION1 = settings.PERMISSION1
PERMISSION2 = settings.PERMISSION2
FOLDER_ID = settings.FOLDER_ID


def gServiceAccount():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """

    if json_keyfile_path:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            json_keyfile_path, scopes=SCOPES,
        )
    else:
        return False

    service = build('drive', 'v3', credentials=credentials)
    return service

'''
Function to Upload Files on GDrive
:Params: instance of request.FILES
'''
def gDriveUpload(f):
    bytesFile = b''
    for chunk in f.chunks():
        bytesFile += chunk

    
    
    file_metadata = {'name': f.name,
                    'parents': [FOLDER_ID],
                    } 
    fileBytes = io.BytesIO(bytesFile)
    media = MediaIoBaseUpload(fileBytes, mimetype='application/octet-stream', chunksize=-1, resumable=True)
    service = gServiceAccount()

    uploadFile = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    fileBytes.close()
    fileId = uploadFile.get('id')
    print('File ID: %s' % fileId)
    
    permission1 = PERMISSION1
    service.permissions().create(fileId=fileId, body=permission1).execute()
    permission2 = PERMISSION2
    service.permissions().create(fileId=fileId, body=permission2).execute()

    get_link = f"https://drive.google.com/file/d/{uploadFile.get('id')}/preview"
    print("url: ", get_link)
    return get_link

