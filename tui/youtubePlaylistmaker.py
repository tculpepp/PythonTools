####################################
# this has been refactored to just hold functions with no execution code
# this takes an HTML input file, scrapes for youtube links, and extracts the 
# video ID's
# Then it creates a new playlist and adds each of the video's from the HTML 
# file to the new playlist.
# Requires: relative path for input file and name for playlist
####################################

import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from bs4 import BeautifulSoup

#open the input file, scrape the IDs & return list
def scrape_video_ids(source_file_path, playlist_name):
    with open(source_file_path) as source:
        soup = BeautifulSoup(source, 'html.parser')
    extracted_id_list = [playlist_name]
    for link in soup.find_all("a"):
        try:
            href = link.get('href')
            if href.startswith('https://www.youtube.com'):
                # print(href)
                extracted_id_list.append(href.split('?v=')[1])
        except:
            pass
    return extracted_id_list

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

# authenticate with the YouTube API & return authentication information
def login():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret_TUIYouTube.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    return youtube

# create a playlist and return the playlist JSON object
def create_playlist(youtube, playlist_title):
  request = youtube.playlists().insert(
      part="snippet,status",
      body={
        "snippet": {
          "title": playlist_title,
          "defaultLanguage": "en"
        },
        "status": {
          "privacyStatus": "public"
        }
      }
  )
  response = request.execute()

  print("Playlist Created: "+response['snippet']['title'])
  return response

# add videos to the created playlist
def add_list_items(youtube, video_list, playlist_id):
  for video_id in video_list:
    try:
      request = youtube.playlistItems().insert(
        part="snippet",
        body={
          "snippet": {
            "playlistId": playlist_id,
            "resourceId": {
              "kind": "youtube#video",
              "videoId": video_id
            }
          }
        }
      )
      response = request.execute()
      print("Video Added: "+response['snippet']['title'])
    except:
      print("Error, video skipped: "+video_id)

# here's where execution actually begins
# source_file = 'CSC330-Reference/CSC330/Modules/Module1/Mod1Background.html'


# video_id_list = scrape_video_ids(source_file, 'test playlist')
# login_data = login()
# playlist_name = video_id_list.pop(0)
# json_data = create_playlist(login_data, playlist_name)
# add_list_items(login_data, video_id_list, json_data['id']) 