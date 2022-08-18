import json
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# SPOTIFY DEV GLOBALS
USERNAME = 'Noahai'
CLIENT_ID = os.getenv('SPOTIFY_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_SECRET')

music_year = input('which year do you want to travel to? Type the date in this format YYYY-MM-DD: ')
PLAYLIST_NAME = f'{music_year} Billboard 100'
response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{music_year}/")
website_html = response.text
soup = BeautifulSoup(website_html, 'html.parser')
all_songs = soup.find_all(name='h3', class_="c-title", id='title-of-a-story')
song_list = [song.getText().replace('\n', '').replace('\t', '').replace('\'', '').replace('\"', '').replace(',', '') for song in all_songs]
song_names = list(dict.fromkeys(song_list))
song_names.remove('Songwriter(s):')
song_names.remove('Producer(s):')
song_names.remove('Imprint/Promotion Label:')
only100_songs = []

for i in range(2, 102):
    only100_songs.append(song_names[i])

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                                               client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri="https://example.com",
                                               scope="playlist-modify-private",
                                               show_dialog="true",
                                               cache_path= 'tokens.txt',)
                    )

user_id = sp.current_user()["id"]
new_playlist = sp.user_playlist_create(user_id, PLAYLIST_NAME, public=False, collaborative= False, description= 'top 100 songs to the date')
playlist_id = new_playlist['id']
print(playlist_id)
song_uris = []

for song in only100_songs:
    result = sp.search(q=f"track:{song} year:{music_year.split('-')[0]}", type='track')
    json_obj = json.dumps(result, indent=4)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

result = sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist_id, tracks=song_uris)