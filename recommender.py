import requests
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

pd.set_option("display.width", 500)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

spotify_data_ = pd.read_csv("last_spotify_data.csv")
imdb_data_ = pd.read_csv("last_imdb_data_only_movies.csv")


# weather with api
def get_weather(city_name):
    api_key = " "  # OpenWeatherMap API anahtarınızı buraya ekleyin

    lat_url = "http://api.openweathermap.org/geo/1.0/direct?"
    lat_response = requests.get(lat_url, params={"q": city_name, "appid": api_key})
    lat_data = lat_response.json()

    if lat_data:
        latitude = lat_data[0]["lat"]
        longitude = lat_data[0]["lon"]

        base_url = "https://api.openweathermap.org/data/2.5/weather?"
        complete_url = base_url + f"lat={latitude}&lon={longitude}&appid={api_key}&units=metric"

        response = requests.get(complete_url)
        weather_data = response.json()

        if "weather" in weather_data:
            main_info = weather_data["weather"][0]["main"]
            description = weather_data["weather"][0]["description"]
            temperature = weather_data["main"]["temp"]
            humidity = weather_data["main"]["humidity"]
            pressure = weather_data["main"]["pressure"]
            wind_speed = weather_data["wind"]["speed"]

        else:
            print("Hava durumu bilgisi bulunamadı.")
    else:
        print("Şehir bulunamadı.")

    return main_info



def get_songs_by_weather(weather_col, tf_idf_col, weather_variable, num_of_recommend):
    """
        Description:
            Bu fonksiyonun amacı, kullanıcıdan alınan hava durumu bilgisi ve veri setimizdeki hava durumu bilgisi arasında cosinüs benzerliğine göre
            girilen veri setinde istenilen sayıda, rastgele olarak, Popularity'e göre azalan şekilde şarkı tavsiyesinde bulunmak.

        Variables:
            dataframe: ilgili veri seti
            weather_col: veri setindeki hava durumu sütunu
            tf_idf_col: tf_idf yöntemiyle ilgili veri setinde, belirtilen sütundaki kelime sıklığını hesaplar
            weather_variable: kullanıcıdan alınan hava durumu bilgisi
            num_of_recommend: tavsiye adedi

    """
    dataframe = spotify_data_

    # kullanıcıdan alınan hava durumu bilgisine göre kendi veri setimizde filtreleme
    filtered_songs = dataframe[(dataframe[weather_col] == weather_variable)]

    # istenilen tavsiye adedi
    num_songs_to_recommend = num_of_recommend

    # rastgele indeksler oluştururken yukarıda filtrelenen şarkıların boyutu kadar oluşturucaz
    num_songs_available = len(filtered_songs)

    # metin
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(filtered_songs[tf_idf_col])

    # benzerliği hesaplama
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # şarkı seçimi için rastgele indeksler oluşturma
    random_indices = np.random.choice(num_songs_available, size=num_songs_to_recommend, replace=False)

    # seçilen şarkı için cosinüs benzerliğine göre sıralanmış şarkı indekslerini alma
    song_indices = cosine_sim[0].argsort()

    # random indices kullanarak şarkıları seçme
    top_songs_indices = song_indices[random_indices][::-1]

    # veri setimizden yukarda oluşturulan şarkıları alma
    top_songs = filtered_songs.iloc[top_songs_indices]

    # Popularity'e göre azalan şekilde sıralama ve indeks'leri resetleme
    top_songs = top_songs.sort_values("Popularity", ascending=False).reset_index()

    # indeks de resetleme işleminden sonra oluşan "index" kolonunu düşürme
    del top_songs["index"]

    # şarkıları yazdırma
    return top_songs[
        ["Track Name", "Artist", "Image", "Album", "Popularity", "Season"]
    ]


def get_movies_by_weather(weather_col, tf_idf_col, weather_variable, num_of_recommend):
    """
        Description:
            Bu fonksiyonun amacı, kullanıcıdan alınan hava durumu bilgisi ve veri setimizdeki hava durumu bilgisi arasında cosinüs benzerliğine göre
            girilen veri setinde istenilen sayıda, rastgele olarak, Rating'e göre azalan şekilde film tavsiyesinde bulunmak.

        Variables:
            dataframe: ilgili veri seti
            weather_col: veri setindeki hava durumu sütunu
            tf_idf_col: tf_idf yöntemiyle ilgili veri setinde, belirtilen sütundaki kelime sıklığını hesaplar
            weather_variable: kullanıcıdan alınan hava durumu bilgisi
            num_of_recommend: tavsiye adedi
    """
    dataframe = imdb_data_
    # kullanıcıdan alınan hava durumu bilgisine göre kendi veri setimizde filtreleme
    filtered_movies = dataframe[(dataframe[weather_col] == weather_variable)]

    # istenilen tavsiye adedi
    num_movies_to_recommend = num_of_recommend

    # rastgele indeksler oluştururken yukarıda filtrelenen filmlerin boyutu kadar oluşturucaz
    num_movies_available = len(filtered_movies)

    # metin
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(filtered_movies[tf_idf_col])

    # benzerliği hesaplama
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # film seçimi için rastgele indeksler oluşturma
    random_indices = np.random.choice(num_movies_available, size=num_movies_to_recommend, replace=False)

    # seçilen film için cosinüs benzerliğine göre sıralanmış film indekslerini alma
    movie_indices = cosine_sim[0].argsort()

    # random indices kullanarak filmleri seçme
    top_movies_indices = movie_indices[random_indices][::-1]

    # veri setimizden yukarda oluşturulan filmleri alma
    top_movies = filtered_movies.iloc[top_movies_indices]

    # Rating'e göre azalan şekilde sıralama ve indeks'leri resetleme
    top_movies = top_movies.sort_values("Rating", ascending=False).reset_index()

    # index de resetleme işleminden sonra oluşan "index" kolonunu düşürme
    del top_movies["index"]

    # filmleri yazdırma
    return top_movies[
        ['Title', 'Year', 'Genre', 'Description', 'Rating', 'Director', 'Votes', "Weather", "Season"]
    ]
