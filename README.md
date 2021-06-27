# Spotify Cluster and Recommender

## Motivation
I was interested in finding music similar to my tastes that I have never heard. I find that Spotify's recommended playlists are either just songs I already have or by the artists I already listen to, but I wanted something more.

## Process
After obtaining my streaming data from Spotify ([How To Request Spotify Data](https://support.spotify.com/us/article/data-rights-and-privacy-settings/)), I setup a pipeline to transform this into a dataframe with audio features for each song. I think performed some data analysis and visualizations on the audio features provided by Spotify. 

I then trained a KMeans clustering model on the audio features. Then, I created a pipeline to get the top 1000 songs (based on Spotify search function) from many years (1960-2009 currently) for many genres of music I like to listen to, transformed this data into it's audio features, and used the KMeans model to predict which cluster these songs go in. 

Then, I used the distance feature from the KMeans model to sort the distance from small to large, and used the Spotify Web API to automatically create a playlist of my 500 most recommended songs (based on the 500 smallest distances to a cluster center).

## Requirements
  * [Requirements](https://github.com/EWiliams0590/Spotify/blob/main/requirements.txt)
## Notebooks and .py Scripts
  * [Helper Functions For Getting Audio Features](https://github.com/EWiliams0590/Spotify/blob/main/DataPipelineFunctions.py)
  * [Get Dataframe with Audio Features and Song Info](https://github.com/EWiliams0590/Spotify/blob/main/GetSongDataFinal.py)
  * [Analysis and Visualization](https://github.com/EWiliams0590/Spotify/blob/main/Final%20Dataset%20and%20Basic%20EDA.ipynb)
  * [Clustering Model](https://github.com/EWiliams0590/Spotify/blob/main/Clustering%20My%20Top%20Songs%20Spotify.ipynb)
  * [Data Collection for Recommended Playlist](https://github.com/EWiliams0590/Spotify/blob/main/GetSongDataFromSearch.py)
  * [Playlist Creator](https://github.com/EWiliams0590/Spotify/blob/main/GetPlaylist.py)
## Tools
### APIs
  * [Spotify Web API](https://developer.spotify.com/documentation/web-api/)
### Python Libraries
  * [Pandas](https://pandas.pydata.org/), [Numpy](https://numpy.org/) - data analysis
  * [Matplotlib](https://matplotlib.org/), [Seaborn](https://seaborn.pydata.org/index.html) - data visualization
  * [Sci-Kit Learn](https://scikit-learn.org/stable/index.html) - KMeans Clustering
  * [Spotipy](https://spotipy.readthedocs.io/en/2.18.0/) - access to Spotify Web API
