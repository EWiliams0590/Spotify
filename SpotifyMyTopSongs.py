import pandas as pd

import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import json
from pprint import pprint

# Get data into a single df

dfs = []

for i in range(3):
	file = f'StreamingHistory{i}.json'
	temp = pd.read_json(file)
	dfs.append(temp)
	
df = pd.concat([dfs[i] for i in range(len(dfs))], ignore_index=True)

track_counts = df.value_counts(['trackName', 'artistName']).to_frame().reset_index()

final_track_df = track_counts.rename(columns= {track_counts.columns[-1]: 'PlayCount'})

top_tracks = final_track_df[:300]

top_tracks.to_csv('TopTracks.csv')