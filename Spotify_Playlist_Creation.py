import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_KEY = os.getenv("CLIENT_KEY")

date = input("Enter the date(format yyyy-mm-dd) :")
date_year = date.split("-")[0]

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
content = response.text

soup = BeautifulSoup(content, "html.parser")

songs_tags = soup.find_all(name = "h3", id = "title-of-a-story")
songs = [song.getText() for song in songs_tags]



code = os.getenv("CODE")


auth = SpotifyOAuth(client_id = CLIENT_ID , client_secret = CLIENT_KEY, scope = "playlist-modify-private", redirect_uri = "http://example.com", 
                            state = None, cache_path = None, requests_timeout = None, username = "Akki")

# app_url = auth.get_authorize_url(state=None)
# print(app_url)


token = auth.get_access_token(code = code, as_dict = False, check_cache = True)



sp = spotipy.Spotify(auth = token)
user_id = sp.current_user()["id"]

playlist = sp.user_playlist_create(user_id, f"Top 100 of the year {date_year}", public=False, description='The top 100 songs of the given year.')
playlist_id = playlist["id"]

track_id_list = []
for song in songs :
    try :
        track = sp.search(f"track: {song}", limit=1, offset=0, type='track', market=None)
        print(track)
    except :
        pass
    else :
        track_id = track["tracks"]["items"][0]["uri"]
        track_id_list.append(track_id)




sp.user_playlist_add_tracks(user = user_id, playlist_id = playlist_id, tracks = track_id_list)









  
