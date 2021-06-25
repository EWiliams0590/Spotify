### Functions to turn Spotify streaming data into 

import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

def create_df(files, N):
    """
    Parameters
    ----------
    files : input files of json data.
    N : minimum number of plays for the song
    
    Returns
    -------
    Writes artist, song, and play count data to csv.
    returns dataframe with just artist and song.
    """
    dfs = []
    
    for file in files:
        temp = pd.read_json(file)
        dfs.append(temp)
    	
    df = pd.concat([dfs[i] for i in range(len(dfs))], ignore_index=True)
    track_counts = df.groupby(['trackName', 'artistName']).size().reset_index()
    track_counts = track_counts.rename({0: 'Play Count'}, axis=1)
    counts_final = track_counts[track_counts['Play Count']>=N]
    
    counts_final.to_csv('ArtistTracksPlayCount.csv', index=False)
    final = counts_final.drop('Play Count', axis=1)
    return final
    
  
def get_artist_song_dict(df):
    """
    Parameters
    ----------
    df : pandas dataframe

    Returns
    -------
    dictionary with keys as artists and values as their songs.

    """
    
    # zip artist and song so they can be searched
    artists = df['artistName'].tolist()
    songs = df['trackName'].tolist()
    artist_song_dict = dict()
    
    for artist, song in zip(artists, songs):
    	if artist in artist_song_dict:
    		artist_song_dict[artist].append(song)
    	else:
    		artist_song_dict[artist] = [song]
            
    return artist_song_dict


def get_song_ids(client_id, client_secret, artist_song_dict):
    """
    Parameters
    ----------
    client_id : client_id from Spotify Developer API
    client_secret :client_secret from Spotify Developer API
    artist_song_dict : Dict with keys as artists and songs as the values.

    Returns
    -------
    list of tuples (artist, song, song_id).

    """
    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    	client_id=client_id, 
    	client_secret=client_secret))

    # Find IDs for the songs
    song_search = list()
    artist = list(artist_song_dict.keys())[0]
    # for artist in list(artist_song_dict.keys())[0]:
    for song in artist_song_dict[artist]:
        if len(sys.argv) > 1:
            name = ' '.join(sys.argv[1:])
        else:
            name = song
        query = artist + ' ' + name
        results = spotify.search(q=query, type='track', limit=1)
        items = results['tracks']['items']
        print(items)
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
                    
    return song_search


def get_audio_analysis(client_id, client_secret, tuples_of_song_info):
    """
    Parameters
    ----------
    client_id : client_id from Spotify Developer API
    client_secret :client_secret from Spotify Developer API
    tuples_of_song_info : list of tuples (artist, song, song_id)

    Returns
    -------
    dict with keys "song by artist" and values are audio analysis.

    """
    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
                           	  client_id=client_id,
                              client_secret=client_secret))
    song_details = dict()
    for artist, track, trackID in tuples_of_song_info:
        if len(sys.argv) > 1:
            tid = sys.argv[1]
        else:
            tid = trackID
        analysis = spotify.audio_features(tid)[0]
        song_details[f'{track} by {artist}'] = analysis
       
    return song_details


def get_final_song_data(song_details, filename):
    """
    Parameters
    ----------
    song_details : Dict of song information
    filename: Filename to write the final csv to.

    Returns
    -------
    writes final song data to a .csv file

    """
    
    df = pd.DataFrame.from_dict(data=song_details, orient='index')
    df.to_csv(filename)
