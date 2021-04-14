# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 22:47:41 2015

@author: lpbrown999 / /u/oiturtlez
"""

import http.client as httplib
import os
import httplib2
import random
import time

from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow, argparser

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
YOUTUBE_UPLOAD_SCOPE = 'https://www.googleapis.com/auth/youtube.upload'
CLIENT_SECRETS_FILE = 'client_secret.json'

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, httplib.NotConnected,
  httplib.IncompleteRead, httplib.ImproperConnectionState,
  httplib.CannotSendRequest, httplib.CannotSendHeader,
  httplib.ResponseNotReady, httplib.BadStatusLine)

httplib2.RETRIES = 1
MAX_RETRIES = 10
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   {}

with information from the Developers Console
https://console.developers.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""".format(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE)))


def get_authenticated_service():
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_UPLOAD_SCOPE, message=MISSING_CLIENT_SECRETS_MESSAGE)
    storage = Storage("storage.json")
    credentials = storage.get()
    args = argparser.parse_args()
    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, args)

    return(build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, http=credentials.authorize(httplib2.Http())))

def initialize_upload(youtube, file, video_title, video_description, tags_list, categoryId, privacy_status):  #authenticated youtube service, file name as string, video title as string, video description as string, tags as list, category numeric id as string
    body=dict(
        snippet=dict(
            title=video_title,
            description= video_description,
            tags=tags_list,
            categoryId=categoryId
        ),
        status=dict(
            privacyStatus=privacy_status
        )
    )
    
    insert_request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=MediaFileUpload(file, chunksize=-1, resumable=True))
    return(resumable_upload(insert_request))

def resumable_upload(insert_request):
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            print("Uploading File")
            status, response = insert_request.next_chunk()
            if 'id' in response:
                print("Video id {} was successfully uploaded.".format(response['id']))
                return(response)
            else:
                exit("The upload failed with an unexpected response: {}".format(response))
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = "A retriable HTTP error {} occurred:\n {}".format(e.resp.status, e.content)
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = "A retriable error occurred: {}".format(e)
        
        if error is not None:
            print(error)
            retry += 1
            if retry > MAX_RETRIES:
                exit("No longer attempting to retry.")
        
            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print("Sleeping {} seconds and then retrying...".format(sleep_seconds))
            time.sleep(sleep_seconds)


def upload(file, **kwargs):
    """Define default arguments in case arguments are not passed to the function."""
    video_title = "Default Title"
    video_description = "Default Description"
    tags_list = []
    categoryId = "20"
    privacy_status = 'public'
    
    """Check if the arguments are passed to the function, and if they are then assign them."""
    
    if 'title' in kwargs:
         video_title = kwargs['title']
    if 'description' in kwargs:
        video_description = kwargs['description']
    if 'tags' in kwargs:
        tags_list = kwargs['tags']
    if 'categoryId' in kwargs:
        categoryId = str(kwargs['categoryId'])
    if 'privacy_status' in kwargs:
        if kwargs['privacy_status'] in VALID_PRIVACY_STATUSES:
            privacy_status = kwargs['privacy_status']
    youtube = get_authenticated_service()
    
    try:  
        response = initialize_upload(youtube, file, video_title, video_description, tags_list, categoryId, privacy_status)
        print(response['id'])
        return(response)
    except HttpError as e:
        print("An HTTP error occured {}".format(e))
 