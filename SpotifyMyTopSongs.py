import pandas as pd

# My Streaming Data is in the Files "StreamingHistoryJson{x}.json" in the same directory,
# where x in range(3)

dfs = []

for i in range(3):
	file = f'StreamingHistory{i}.json'
	temp = pd.read_json(file)
	dfs.append(temp)
	
df = pd.concat([dfs[i] for i in range(len(dfs))], ignore_index=True)

track_counts = df.value_counts(['trackName', 'artistName']).to_frame().reset_index()

final_track_df = track_counts.rename(columns= {track_counts.columns[-1]: 'PlayCount'})

top_100_tracks = final_track_df[:300]

top_100_tracks.to_csv('Top100Tracks.csv', index=False)
