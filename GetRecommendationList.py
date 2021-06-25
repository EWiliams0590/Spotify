import pandas as pd

from joblib import load

df = pd.read_csv('tracks.csv')

# fix the df
columns = ['id', 'name', 'artists', 'danceability','energy', 'loudness', 
           'speechiness', 'acousticness', 'liveness', 'valence', 'tempo']

fixed = df[columns]

# fix artists column
fixed['artists'] = fixed['artists'].str.split(',').str[0].str.replace("[\['\]]", "")

# drop duplicates based on name and artists
fixed.drop_duplicates(['name', 'artists'], keep='first', inplace=True)

final = fixed.set_index(['name', 'artists', 'id'])

model = load('KMeansModel.joblib')

clusters = model.predict(final)

distances = model.transform(final)
mins = []

for i in range(distances.shape[0]):
    curr = distances[i]
    min_distance = min(curr)    
    mins.append(min_distance)
    
results = pd.DataFrame(index=final.index)

results['Cluster'] = clusters
results['Distance'] = mins

results_sorted = results.sort_values(by='Distance', ascending=True)

results_sorted.to_csv('RankedRecommendedSongs2020.csv')