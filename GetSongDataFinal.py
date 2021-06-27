### Composes the data pipeline functions into one function
### to transform streaming data into a single dataframe with the
### audio features for each song that meets a minimum number of plays.

from DataPipelineFunctions import create_artist_song_df, get_audio_analysis
from DataPipelineFunctions import get_song_ids


def get_song_data_for_analysis(files, N, spotify, filename):
    """
    Parameters
    ----------
    files : files where streaming data comes from
    N : minimum number of play count
    client_id :  client_id from spotify developer api
    client_secret : client_secret from spotify developer api

    Returns
    -------
    writes finalized dataframe to "filename"
    and returns the dataframe with audio features.
    """
    # create the dict and save a csv for the playcounts
    artist_song_counts_df = create_artist_song_df(files, N)
    
    # get audio analysis data
    song_ids = get_song_ids(spotify, artist_song_counts_df)
    audio_final_df = get_audio_analysis(spotify, song_ids)
    
    final_df = audio_final_df.merge(song_ids, how='inner', on='id')
    
    final_df.to_csv(filename, index=False)
    return final_df
