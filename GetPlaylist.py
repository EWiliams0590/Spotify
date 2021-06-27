### Creates a playlist based on the clustering model from a file
### containing the audio features for songs. Must provide the full
### amount of features and track id.

import pandas as pd
import numpy as np

def get_recommendation_list(df, model):
    """
    Parameters
    ----------
    df : dataframe of audio features with track id
    model: clustering model to find cluster and distance for each song

    Returns
    -------
    dataframe with columns as (id, distance), sorted by distance ascending.
    """
    df = df.set_index('id')
    distances = model.transform(df)
    if 'instrumentalness' in df.columns:
        df.drop('instrumentalness', axis=1, inplace=True)
        
    # get the minimum distance 
    mins = []
    for i in range(distances.shape[0]):
        curr = distances[i]
        min_distance = min(curr)    
        mins.append(min_distance)
        
    data = np.column_stack((df.index, mins))
    columns = ['id', 'distance']
    results = pd.DataFrame(data=data, columns=columns)  
    
    results_sorted = results.sort_values(by='distance', ascending=True)
    
    return results_sorted


def create_recommended_playlist(df, spotify, user, playlist_name, N):
    """
    Parameters
    ----------
    df : dataframe of track ids
    spotify: authorization token to create playlist for user
    user: spotify username
    playlist_name: name of created playlist
    N: length of playlist
    
    Returns
    -------
    creates a playlist for the given user
    """
    spotify.user_playlist_create(user, playlist_name)
    playlist = spotify.current_user_playlists(limit=1) # get created playlist
    playlist_id = playlist['items'][0]['id']
    
    for i in range(0, N, 100): # can only add 100 at a time
        song_ids = df['id'][i:i+100]
        spotify.playlist_add_items(playlist_id, song_ids)
        
        
    
    

