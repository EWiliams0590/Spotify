### Functions to turn Spotify streaming data into audio analysis data

### The function create_artist_song_df is rather specific, but if you get your
### streaming data from Spotify and store the files in the working directory,
### it will transform this into a dataframe of the artist and track with
### the play count of each.

### The function get_song_ids will get the song idea for a given artist and song
### pair. The track count is not needed (I just wanted it to store).

### The function get_audio_analysis will return a dataframe with the spotify
### audio features given the track ids.

import pandas as pd
import numpy as np


def create_artist_song_df(files, N=1):
    """
    Parameters
    ----------
    files : input files of json data.
    N : minimum number of plays for the song to be stored in the df
    filepath: filepath to save PlayCount data
    
    Returns
    -------
    pandas df with cols ['trackName', 'artistName', 'playCount']
    """
    dfs = []
    
    for file in files:
        temp = pd.read_json(file)
        dfs.append(temp)
    	
    df = pd.concat([dfs[i] for i in range(len(dfs))], ignore_index=True)
    track_counts = df.groupby(['trackName', 'artistName']).size().reset_index()
    track_counts = track_counts.rename({0: 'playCount'}, axis=1)
    artist_song_counts_df = track_counts[track_counts['playCount']>=N]
    return artist_song_counts_df


def get_song_ids(spotify, artist_song_counts_df):
    """
    Parameters
    ----------
    spotify :  spotify developer authorization manager
    artist_song_dict : Dict with keys as artists and songs as the values.

    Returns
    -------
    pandas df with columns (artistName, trackName, id).

    """
    artists = artist_song_counts_df['artistName']
    tracks = artist_song_counts_df['trackName']
    track_ids = []
    for artist, track in zip(artists, tracks):
        query = artist + ' ' + track
        results = spotify.search(q=query, type='track', limit=1, offset=0, market='US')
        items = results['tracks']['items']
        if len(items) > 0:
            track_id = results['tracks']['items'][0]['id']
            track_ids.append(track_id)
        else:
            track_ids.append(np.nan)
    
    artist_song_counts_df['id'] = track_ids
    artist_song_counts_df.dropna(axis=0, inplace=True)
    return artist_song_counts_df
   

def get_audio_analysis(spotify, artist_song_counts_df):
    """
    Parameters
    ----------
    spotify :  spotify developer authorization manager
    artist_song_df : pandas dataframe with columns (artistName, trackName, id)

    Returns
    -------
    pandas dataframe of song analysis with ids.
    """
    rows = []
    batch_size = 100 # max number queries allowed per batch
    
    for i in range(0, artist_song_counts_df.shape[0], batch_size):
        batch_ids = artist_song_counts_df.iloc[i: i+batch_size]['id']
        audio_results = spotify.audio_features(batch_ids)
        for i, t in enumerate(audio_results):
            if t == None: # no audio results
                continue
            else:
                rows.append(t)
                
    
    df_audio_features = pd.DataFrame.from_dict(rows)
    # Remove unneeded columns
    columns_to_drop = ['key', 'mode', 'type', 'uri', 'track_href',
                       'analysis_url', 'duration_ms', 'time_signature',
                       'instrumentalness']
    
    df_audio_final = df_audio_features.drop(columns_to_drop, axis=1)
    return df_audio_final       
