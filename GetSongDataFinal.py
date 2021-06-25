from DataPipelineFunctions import create_artist_song_dict, get_audio_analysis
from DataPipelineFunctions import get_final_song_data, get_song_ids


def get_song_data_for_analysis(files, N, client_id, client_secret, filename):
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
    """
    # create the dict and save a csv for the playcounts
    counts_df, artist_song_dict = create_artist_song_dict(files, N)
    
    # get audio analysis data
    song_ids = get_song_ids(CLIENT_ID, CLIENT_SECRET, artist_song_dict)
    song_details = get_audio_analysis(CLIENT_ID, CLIENT_SECRET, song_ids)
    final_song_data = get_final_song_data(song_details)
    
    # combine the audio analysis with play count data
    counts_df['index'] = counts_df['trackName'] + ' by ' + counts_df['artistName']
    combined = final_song_data.merge(counts_df, how='inner')
    
    cols_to_keep = ['danceability', 'energy', 'loudness', 'speechiness', 
                    'acousticness', 'instrumentalness', 'liveness',
                    'valence', 'tempo', 'Play Count', 'index']
    
    final = combined[cols_to_keep].rename({'index': 'Song Info'}, axis=1).set_index('Song Info')
    
    final.to_csv(filename)



files = [f'StreamingHistory{i}.json' for i in range(3)]
N = 10 # lower bound for number of plays
CLIENT_ID = '9c6a8972ab4448a8a8a7a13b8311dd94'
CLIENT_SECRET = '911862d3fa41472da3a7577d30ff5f63'
filename = f"FinalSongData{N}.csv"

get_song_data_for_analysis(files, N, CLIENT_ID, CLIENT_SECRET, filename)