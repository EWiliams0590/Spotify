import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials

import pandas as pd
import json

from pprint import pprint

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
	client_id='', 
	client_secret=''))

df = pd.read_csv('Top100TrackWithIDNoPlayCount.csv')

# danceability = []
# energy = []
# key = []
# loudness = []
# mode = []
# speechiness = []
# acousticness = []
# instrumentalness = []
# liveness = []
# valence = []
# tempo = []
# duration = []
# time_signature = []

song_details = dict()

for artist, track, trackID in zip(df['artistName'], df['trackName'], df['trackID']):
	if len(sys.argv) > 1:
		tid = sys.argv[1]
	else:
		tid = trackID


	analysis = spotify.audio_features(tid)

	song_details.append(analysis)


pprint(song_details)


# with open('SongDetails.json', 'w') as f:
# 	json.dump(song_details, f, indent=4)




