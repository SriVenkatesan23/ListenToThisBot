import praw
import httplib2
import os
import sys
from urllib.parse import urlparse
from urllib.parse import parse_qs
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser
from oauth2client.tools import run_flow
from datetime import datetime



r = praw.Reddit(user_agent='LTTscraper')

print("Enter name of subreddit")
sub = input()

submissions = r.get_subreddit(sub).get_top_from_week(limit=25)
CLIENT_SECRETS_FILE = "keys.json"
MISSING_CLIENT_SECRETS_MESSAGE = """
To make this sample run you will need to populate the client_secrets.json file
found at:
   %s
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
  message=MISSING_CLIENT_SECRETS_MESSAGE,
  scope=YOUTUBE_READ_WRITE_SCOPE)

storage = Storage("%s-oauth2.json" % sys.argv[0])
credentials = storage.get()

if credentials is None or credentials.invalid:
  flags = argparser.parse_args()
  credentials = run_flow(flow, storage, flags)

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
  http=credentials.authorize(httplib2.Http()))

now = datetime.now();
month = now.month
year = now.year
day = now.day

playlists_insert_response = youtube.playlists().insert(
  part="snippet,status",
  body=dict(
    snippet=dict(
      title="%s: Week of %s/%s/%s" %(sub,month,day,year) ,
      description="A private playlist containing the week's top songs from r/%s" %(sub)
    ),
    status=dict(
      privacyStatus="private"
    )
  )
).execute()

def add_video(youtube, videoID, playlistID):
    add_video_request = youtube.playlistItems().insert(
        part="snippet",
        body={
            'snippet': {
                'playlistId': playlistID,
                'resourceId': {
                    'kind': 'youtube#video',
                    'videoId': videoID
                }
            }
        }
    ).execute()

def video_id(link):

    query = urlparse(link)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    return None


for s in submissions:
    if "youtube" in s.url:
        add_video(youtube, video_id(s.url), playlists_insert_response["id"])
