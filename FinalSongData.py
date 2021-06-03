import pandas as pd

ser = pd.read_json('SongDetails.json', typ='series')

data = ser.values

data_dict = dict()

N = len(data)

single_song_data = data[0][0]

for i in range(N):
	song_data = data[i][0]
	for k, v in song_data.items():
		if k in data_dict:
			data_dict[k].append(v)
		else:
			data_dict[k] = [v]


final_song_data = pd.DataFrame.from_dict(data=data_dict).set_index('id')

final_song_data.to_csv('FinalSongData.csv')
