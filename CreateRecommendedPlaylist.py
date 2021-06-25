import pandas as pd
import spotipy

token = 'BQB5OVs1IicnsRrxIButqMU6xIRsh-j755sP9-2rI6vE-4EN8_HY4zk2FARjaK-p_ndIW-f5uU-GTgnbYtlLAiqOCINVd3VtuphUCQBgb-zKrluiXn06sPKQvOy6YDwCWCGk33Jlp4ElhCPOd8Z6IDAmOycpDNlg_zEokL3DyynPwkMOr_3_WSAzL-KohQTOgI8qIUaFXS8-p8A5Q5RSiQIXPBE'
sp = spotipy.Spotify(auth=token)

user = 'charity4thepoor'

sp.user_playlist_create(user, 'Recommend')

recommended = sp.current_user_playlists(limit=1)

playlist_id = recommended['items'][0]['id']

df = pd.read_csv('RankedRecommendedSongs2020.csv')


for i in range(5):
    song_ids = df['id'][i*100:(i+1)*100]
    sp.playlist_add_items(playlist_id, song_ids)