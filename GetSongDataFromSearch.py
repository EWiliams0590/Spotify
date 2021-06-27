### Get the song, track, and track id for songs from a spotify search
### for provided years and genres. Note that the amount of searching done per
### genre/year combination is 1000.

import numpy as np
import pandas as pd

def get_track_id(spotify, years, genres, N):
    """
    Parameters
    ----------
    spotify : authorization access token from Spotify Account
    years: a list of years to search
    genres: a list of genres wished to retrieve results
    N : number of songs per year (maximum) <= 1000

    Returns
    -------
    Gets first N songs from spotify search for the given years.
    Writes to a single dataframe with columns of artistName, trackName, and id.
    Note the id is for the song.
    """
    if N > 1000:
        print("N cannot exceed 1000")
        return
    artistName = []
    trackName = []
    trackID = []
    for genre in genres:
        for year in years:
            for i in range(0, N, 50):
                results = spotify.search(q=f'year:{year} genre:{genre}', type='track', limit=50, 
                                         offset=i, market='US')
                for j, t in enumerate(results['tracks']['items']):
                    artistName.append(t['artists'][0]['name'])
                    trackName.append(t['name'])
                    trackID.append(t['id'])
                
    data = np.column_stack((artistName, trackName, trackID))
    columns = ['artistName', 'trackName', 'id']         
    df = pd.DataFrame(data=data, columns=columns)
    df.drop_duplicates(subset=['artistName', 'trackName'], inplace=True)
    df.to_csv(f"Songs{years[0]}to{years[-1]}.csv", index=False)
    return df



                                