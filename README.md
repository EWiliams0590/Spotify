# Spotify Cluster and Recommender
I obtained my Spotify streaming data over the course of a year. By using Spotipy, I got the audio analysis for all songs listened to at least 10 times throughout the dataset.

I proceeded to run kmeans clustering to cluster the data.

Once the clustering model was trained, I predicted on the dataset "Spotify Dataset 1922-2021, ~600k Tracks" by Yamac Eren Ay on Kaggle.

From the predictions, I got the 500 closest songs to a cluster center and automated adding them to my Spotify playlist.

### Results
As I discussed in the EDA notebook above, I had some reservations about how Spotify figured out the audio analysis data, but I am pleasantly surprised by the results. I have found many songs by bands that I have never heard of that I enjoy.


