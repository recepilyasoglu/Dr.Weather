from bs4 import BeautifulSoup
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


# weather with Google search
def weather():
    city = input("Enter the Name of City ->  ")
    city = city + " weather"

    city = city.replace(" ", "+")
    res = requests.get(
        f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8',
        headers=headers)
    print("Searching...\n")
    soup = BeautifulSoup(res.text, 'html.parser')
    location = soup.select('#wob_loc')[0].getText().strip()
    time = soup.select('#wob_dts')[0].getText().strip()
    info = soup.select('#wob_dc')[0].getText().strip()
    weather = soup.select('#wob_tm')[0].getText().strip()

    city_name = city.split("+")

    print("####### " + city_name[0], "" + location + " #######", "\n", time, "\n", info,
          "\n", weather + "°C", "\n", "İyi Günler :)")


weather()


# weather with api
def get_weather(city_name):
    api_key = "414ac3ef8077653d4bbf40735333545d"  # OpenWeatherMap API anahtarınızı buraya ekleyin

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

            # print("Hava Durumu Bilgisi")
            # print(f"Şehir: {city_name}")
            # print(f"Ana Durum: {main_info}")
            # print(f"Hava Durumu Açıklaması: {description}")
            # print(f"Sıcaklık: {temperature} °C")
            # print(f"Nem: {humidity}%")
            # print(f"Rüzgar Hızı: {wind_speed} m/s")
        else:
            print("Hava durumu bilgisi bulunamadı.")
    else:
        print("Şehir bulunamadı.")

    return main_info

city = input("Şehir adını girin: ")

weather = get_weather(city)

weather

# IMDB Dataset Workplace
df = pd.read_csv("imdb_movies.csv", index_col=0)
df.head()


# EDA
def get_stats(dataframe):
    return print("###### İlgili veri setinin ilk 5 satırı ###### \n", dataframe.head(), "\n",
                 "###### İlgili veri setinin boyutu ###### \n", dataframe.shape, "\n",
                 "###### İlgili veri setindeki değişkenlerin veri tip'leri ###### \n", dataframe.dtypes, "\n",
                 "###### İlgili veri setinin betimsel istatistiği ###### \n", dataframe.describe().T, "\n",
                 "###### İlgili veri setindeki null değerlerin sayısı ###### \n", dataframe.isnull().sum())


get_stats(df)

# ilgili iş problemimizde Genre ve Rating kullanıcıya içerik tavsiyesinde bulunurken,
# doğrudan önemli değişkenler olduğu için direkt düşürüldü, Director de 80 küsür dü o da düşürüldü.

df.isnull().sum()

df.dropna(subset=["Genre", "Rating"], inplace=True)
df.shape

# Gross değişkenindeki NAN değerleri doldurma
df["Gross"].head()

# ortalamasını almadım, çünkü her filmin Gross miktarı filme göre değişebilir
# onun için 0 ile doldurmak daha mantıklı geldi

df["Gross"].fillna('0', inplace=True)

df["Gross"].head()

df.isnull().sum()


# Feature Engineering

df["Weather"].value_counts()

# gelen Hava Durumu AP içerisindeki json dosyasında yer alan 8 farklı hava durumu bilgisinden yola çıkarak
# oluşturulan mevsim'lere ait keyword'ler

spring_keywords = ["Rain", "Drizzle", "Clouds", "Fog"]
summer_keywords = ["Clear", "Thunderstorm", "Clouds"]
autumn_keywords = ["Rain", "Mist", "Drizzle", "Fog", "Clouds"]
winter_keywords = ["Snow", "Mist", "Fog", "Clouds"]


# Mevsimleme çalışması
def get_seasons(dataframe, weather_col, season_col, seasons_list, spring_key, summer_key, autumn_key, winter_key):
    """
            Amaç: Verilen veri setindeki Hava Durumu değişkeni içinmevsim keywordlerinden yola çıkarak mevsimleme çalışması.
                Not: Fonksiyon 4 mevsim üzerine kurulmuştur, farklı sayı da mevsim istenirse fonksiyon üzreinde düzenlemeler yapılabilir.

            Variables;
                dataframe: ilgili veri seti,
                weather_col: veri setindeki hava durumu sütunu,
                season_col: atanması istenilen mevsim sütunu,
                seasons_list: istenilen mevsimler
                spring_key: İlkbahar keyword
                summer_key: yaz keyword
                autumn_key: sonbahar keyword
                winter_key: kış keyword
        """

    conditions = [
        dataframe[weather_col].isin(spring_key),
        dataframe[weather_col].isin(summer_key),
        dataframe[weather_col].isin(autumn_key),
        dataframe[weather_col].isin(winter_key)
    ]

    choices = [seasons_list[0:1], seasons_list[1:2], seasons_list[2:3], seasons_list[3:4]]
    dataframe[season_col] = np.select(conditions, choices, default='')

    return dataframe


get_seasons(df, "Weather", "Season", ["Spring", "Summer", "Autumn", "Winter"],
            spring_keywords, summer_keywords, autumn_keywords, winter_keywords)

df["Weather"].value_counts()

df["Season"].value_counts()

# del df["Season"]

df.shape


# yılın iki mevsiminde de tekrar eden aynı hava durumları için
def season_for_weathers(dataframe, weather_col, variable, season_col, wanted_count, wanted_season1, wanted_season2):
    """
        Amaç: Farklı mevsimler de aynı hava durumunun gözlemlenmesi üzerine, verile hava durumu değikeninin,
        istenilen mevsimlere eşit bir şekilde rastgele atamasını sağlamak. Böylelikle hava durumu değişkeninin,
        yalnızca bir mevsim de görünmesini engellemek.
        Variables;
            dataframe: ilgili veri seti,
            weather_col: veri setindeki hava durumu sütunu,
            variable: hava durumu değişkeni,
            season_col: atanması istenilen mevsim sütunu,
            wanted_count: kaç eşit parçaya bölünmek istediği (Not: default olarak 2'ye bölünmüştür, farklı sayılar da işlem gerekir)
            wanted_season1: istenilen birinci mevsim
            wanted_season2: istenilen ikinci mevsim
    """

    count = (dataframe[weather_col] == variable).sum()

    variable_per_season = count // wanted_count

    variable_indices = np.random.choice(dataframe[dataframe[weather_col] == variable].index, size=count, replace=False)

    dataframe.loc[variable_indices[:variable_per_season], season_col] = wanted_season1
    dataframe.loc[variable_indices[variable_per_season:], season_col] = wanted_season2

    return print("####### İlgili Hava Durumu ve Ait Olduğu Mevsim #######" "\n", dataframe[[weather_col, season_col]])


season_for_weathers(df, "Weather", "Rain", "Season", 2, "Spring", "Autumn")
season_for_weathers(df, "Weather", "Fog", "Season", 2, "Spring", "Autumn")
season_for_weathers(df, "Weather", "Thunderstorm", "Season", 2, "Spring", "Summer")

df[["Weather", "Season"]].value_counts()

df.head()


# yılın her mevsiminde tekrar eden hava durumu
def season_for_every_weather(dataframe, weather_col, variable, season_col, wanted_count, seasons_list):
    """
        Amaç: Her mevsimde görülebilen hava durumu için yazılmıştır, önceki fonksiyon ile arasındaki fark; Hava Durumunu 4'e bölüyor olması
        çünkü belirtilen Hava Durumunun her mevsim de görüldüğü tespit edilmiştir.
        Farklarından bir diğeri indexleme üzerinde np shuffle kullanarak karıştırılıyor seçip yapılıyor oluşu.
        Dilimleme yaparken de, 4'e bölünme durumunu dikkate alarak gerçekleştirilmiştir.
        Variables;
            dataframe: ilgili veri seti,
            weather_col: veri setindeki hava durumu sütunu,
            variable: hava durumu değişkeni,
            season_col: atanması istenilen mevsim sütunu,
            wanted_count: kaç eşit parçaya bölünmek istediği
            seasons_list = istenen mevsimlerin list halde girilmesi
    """

    count = (dataframe[weather_col] == variable).sum()

    variable_per_season = count // wanted_count

    variable_indices = dataframe[dataframe[weather_col] == variable].index

    variable_indices_np = variable_indices.to_numpy()

    np.random.shuffle(variable_indices_np)

    variable_indices_shuffled = pd.Index(variable_indices_np)

    dataframe.loc[variable_indices_shuffled[:variable_per_season], season_col] = seasons_list[
        0]  # dilimleme de hata almamak için [0] tarzda kullandım
    dataframe.loc[variable_indices_shuffled[variable_per_season:2 * variable_per_season], season_col] = seasons_list[1]
    dataframe.loc[variable_indices_shuffled[2 * variable_per_season:3 * variable_per_season], season_col] = \
    seasons_list[2]
    dataframe.loc[variable_indices_shuffled[3 * variable_per_season:], season_col] = seasons_list[3]

    return print("####### İlgili Hava Durumu ve Ait Olduğu Mevsim #######" "\n", dataframe[[weather_col, season_col]])


season_for_every_weather(df, "Weather", "Clouds", "Season", 4, ["Spring", "Summer", "Autumn", "Winter"])

df[["Weather", "Season"]].value_counts()

df.Season.value_counts()

df.isnull().sum()

df = df.reset_index()
del df["index"]

df.shape

# İçerisinde Hint ifadesini barındıran filmleri ayıklamak
indian_words = ["India", "Hint", "Bollywood", "india"]
filtre = df['Description'].str.contains('|'.join(indian_words), case=False)

indian_movies = df[filtre]

indian_movies = indian_movies.reset_index()
# del indian_movies["index"]

indian_movies.head()
indian_movies.shape

indian_movies["Rating"].mean()
indian_movies["Rating"].max()

indian_movies.to_csv("budabuda.csv")

# veri setimizden hintli filmleri çıkarma
df = df[~filtre]

# indeksleri resetleme
df = df.reset_index()
# del df["index"]

df.shape

df.head(75)
df.tail(75)

df[["Weather", "Season"]].value_counts()

# api den gelen, hava durumuna göre en yüksek rating ortalamaları
df.groupby(["Weather", "Season"]).agg({"Rating": "mean"}).sort_values("Rating", ascending=False)

df.groupby(["Season", "Genre"]).agg({"Rating": "mean"}).sort_values("Rating", ascending=False)

df["Genre"].value_counts()

df[df["Rating"] > 7.0].count()

df
df.head()
df.shape
df.columns

# veri setini kaydetme
# df.to_csv("imdb_data_with_season.csv")


# Filtreleme işlemleri

df.shape

movie_df = df[df["Rating"] > 7.0]

movie_df.shape

movie_df[["Weather", "Season"]].value_counts()

unnecessary_categories = ("Documentary", "Short", "Animation", "Reality-TV",
                          "Game-Show", "Game", "Music", "Talk-Show")


movie_df_ = movie_df[~(movie_df["Genre"].str.startswith(unnecessary_categories))]

movie_df_.shape

movie_df_[["Weather", "Season"]].value_counts()


movie_df_.head(15)

movie_df_.dtypes


# Votes da filtreleme verimizi çok düşürüyor

# movie_df_votes = movie_df_[movie_df_["Votes"] > 500]

# movie_df_votes.shape
#
# movie_df_votes.Weather.value_counts()
#
# movie_df_votes.sort_values(by="Rating", ascending=False).head(10)


# movie_df_votes = movie_df_votes.reset_index()
#
# del movie_df_votes["index"]
#
# movie_df_votes.head(10)
#
# movie_df_votes[movie_df_votes["Title"] == "Red Dead Redemption II"].Description


movie_df_[movie_df_["Title"] == "Red Dead Redemption II"]

movie_df_.to_csv("new_imdb_data_only_movies.csv")


# Filter the Dataset
filtered_movies = movie_df_[(movie_df_['Weather'] == weather)]

# Text Representation
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(filtered_movies['Description'])

# Calculate Similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Rank and Recommend
# Assuming we want to recommend top 5 movies
top_movies_indices = cosine_sim[0].argsort()[-5:][::-1]  # Change the index [0] to the user's preferred movie index
top_movies = filtered_movies.iloc[top_movies_indices]

# Display Recommendations
print("Recommended Movies:")
print(top_movies[['Title', 'Genre', 'Rating', 'Description', 'Director', 'Votes', 'Gross', "Weather", "Season"]])


# Spotify Workplace
spotify_df = pd.read_csv("spotify_weather_data.csv")

spotify_df.head()
spotify_df.shape
spotify_df.isnull().sum()
spotify_df.describe().T


# EDA
# 1 tane eksik değer olduğu için (Image) direkt düşürdüm
spotify_df.dropna(inplace=True)

spotify_df.isnull().sum()

spotify_df["Weather"].value_counts()


# Feature Engineering

# imdb deki mevsileme işleminin spotify için tekrarlanması
get_seasons(spotify_df, "Weather", "Season", ["Spring", "Summer", "Autumn", "Winter"], spring_keywords, summer_keywords,
            autumn_keywords, winter_keywords)

spotify_df[["Weather", "Season"]].value_counts()

# tekrar eden hava durumları için yazdığım fonksiyonu çağırıp mevsimleme işlemi için
season_for_weathers(spotify_df, "Weather", "Rain", "Season", 2, "Spring", "Autumn")
season_for_weathers(spotify_df, "Weather", "Fog", "Season", 2, "Spring", "Autumn")
season_for_weathers(spotify_df, "Weather", "Drizzle", "Season", 2, "Spring", "Autumn")
season_for_weathers(spotify_df, "Weather", "Thunderstorm", "Season", 2, "Spring", "Summer")

spotify_df[["Weather", "Season"]].value_counts()

# yılın 4 mevsiminde de tekrar eden hava durumu için
season_for_every_weather(spotify_df, "Weather", "Clouds", "Season", 4, ["Spring", "Summer", "Autumn", "Winter"])

spotify_df[["Weather", "Season"]].value_counts()

spotify_df.head()

spotify_df.to_csv("spotify_data_with_season.csv")

# Popularity'si 75 den büyük olanları kullanıcıya tavsiye etme kararı aldık
spotify_new_df = spotify_df[spotify_df["Popularity"] > 75]

spotify_new_df = spotify_new_df.reset_index()

# del spotify_new_df["index"]

spotify_new_df.head()

spotify_df[spotify_df["Popularity"] > 80].Weather.value_counts()

df.groupby(["Weather", "Season"]).agg({"Popularity": "mean"}).sort_values("Rating", ascending=False)

spotify_new_df.to_csv("spotify_data_by_popularity.csv")


spotify_data_ = pd.read_csv("spotify_data_by_popularity.csv", index_col=0)
spotify_data_.head()

spotify_data_[spotify_data_["Popularity"] > 75].Weather.value_counts()

spotify_data_.sort_values(by="Popularity", ascending=False)



unnecessary_categories = ("Documentary", "Short", "Animation", "Reality-TV",
                          "Game-Show", "Game", "Music", "Talk-Show")

unwanted_name = []

for i in spotify_data_["Track Name"]:
    if "Remix" in i:
        unwanted_name.append(i)

spotify_data_ = []

movie_df_ = movie_df[~(movie_df["Genre"].str.startswith(unnecessary_categories))]


