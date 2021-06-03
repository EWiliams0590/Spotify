import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials

import pandas as pd
import json

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
	client_id='9c6a8972ab4448a8a8a7a13b8311dd94', 
	client_secret='911862d3fa41472da3a7577d30ff5f63'))

df = pd.read_csv('TopTracksWithID.csv')

song_details = dict()

for artist, track, trackID in zip(df['artistName'], df['trackName'], df['trackID']):
	if len(sys.argv) > 1:
		tid = sys.argv[1]
	else:
		tid = trackID


	analysis = spotify.audio_features(tid)

	song_details[f'{track} by {artist}'] = analysis

with open('SongDetails.json', 'w') as f:
	json.dump(song_details, f, indent=4)




