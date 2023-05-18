import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv

client_id = ''
client_secret = ''

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


playlist_data = [
    {'id': 'https://open.spotify.com/playlist/1ciUxmN0q0dcsNZDY1e1aq?si=b01cbe4ef3b04779', 'name': 'Fog'},
    {'id': 'https://open.spotify.com/playlist/6v623R4f14wpuWvfJHdDwD?si=48b520e24a4c4508', 'name': 'Mist'},
    {'id': 'https://open.spotify.com/playlist/4i4myKpou7R3MmyIdZJo67?si=b27984504d9c4014', 'name': 'Rain'},
    {'id': 'https://open.spotify.com/playlist/0RBNnOZoPVOtSAnlGpZ5Qh?si=9a9e5a9a491b4ce9', 'name': 'Snow'},
    {'id': 'https://open.spotify.com/playlist/5FrzmZWshWRZD1p8XSn348?si=129253df78864731', 'name': 'Drizzle'},
    {'id': 'https://open.spotify.com/playlist/3RaTJ4Y4JICc1z5n1ceMca?si=0a95252d7b5249b1', 'name': 'Thunderstorm'},
    {'id': 'https://open.spotify.com/playlist/055NUqz26MtiebomXn62YX?si=3ac2b585a1604881', 'name': 'Clouds'},
    {'id': 'https://open.spotify.com/playlist/00qtXo3lYWZTWvdd3mKMH2?si=d6def011ba744e7b', 'name': 'Clear'}
]

track_list = []

for playlist in playlist_data:
    playlist_id = playlist['id']
    playlist_name = playlist['name']
    offset = 0
    limit = 100

    while True:
        results = sp.playlist_tracks(playlist_id, offset=offset, limit=limit)

        for item in results['items']:
            track = item.get('track')
            if track is not None:
                images = track['album'].get('images', [])
                image_url = images[0]['url'] if images else None

                track_list.append({
                    'Weather': playlist_name,
                    'Track Name': track.get('name'),
                    'Artist': track['artists'][0]['name'],
                    'Album': track['album']['name'],
                    'Image': image_url,
                    'Popularity': track['popularity']
                })

        if results['next']:
            offset += limit
        else:
            break


# Popülarite puanı, Spotify'ın parçanın aldığı çalma sayısı ve bu çalmaların ne kadar yeni olduğu gibi çeşitli faktörlere dayalı olarak hesapladığı bir ölçümdür.
# 0 ile 100 arasında bir değerdir ve 100 en yüksek popülerlik seviyesini temsil eder.
# Popülerlik puanı, bir çalma listesi veya albümdeki farklı parçaların göreceli popülerliğini belirlemede yararlı olabilir.
# Bir parçanın ne sıklıkta çalındığına dair bir gösterge sağlar ve kullanıcıların trend olan veya popüler şarkıları keşfetmesine yardımcı olabilir.


filename = 'spotify_weather_playlist.csv'
columns = ['Weather', 'Track Name', 'Artist', 'Album', 'Image', 'Popularity']

with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=columns)
    writer.writeheader()
    writer.writerows(track_list)
