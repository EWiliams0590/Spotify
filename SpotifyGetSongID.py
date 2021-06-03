import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import json
from pprint import pprint


spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
	client_id='9c6a8972ab4448a8a8a7a13b8311dd94', 
	client_secret='911862d3fa41472da3a7577d30ff5f63'))


# Open File to get Top Songs
df = pd.read_csv('TopTracks.csv')

# zip artist and song so they can be searched
artists = df['artistName'].tolist()
songs = df['trackName'].tolist()

artist_song_dict = dict()

for artist, song in zip(artists, songs):
	if artist in artist_song_dict:
		artist_song_dict[artist].append(song)
	else:
		artist_song_dict[artist] = [song]

# Find IDs for the songs
song_search = list()

for artist in artist_song_dict:
	for song in artist_song_dict[artist]:
		if len(sys.argv) > 1:
			name = ' '.join(sys.argv[1:])
		else:
			name = song

		query = artist + ' ' + name
		results = spotify.search(q=query, type='track', limit=10)

		items = results['tracks']['items']


		N = len(items)

		if N == 0:
			continue
		else:
			for i in range(N):
				info = items[i]
				track_id = info['id']
				artist_data = info['album']['artists']
				search_artist = artist_data[0]['name']

				if search_artist == artist:
					song_search.append((artist, name, track_id))
					break


search_df = pd.DataFrame(data=song_search, columns=['artistName', 'trackName', 'trackID'])

search_df.to_csv('TopTracksWithID.csv', index=False)