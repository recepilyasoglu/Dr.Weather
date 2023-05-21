import requests
from bs4 import BeautifulSoup
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 500)


def scrape_movies_for_keyword(weather, keyword):
    """
    Belirli bir anahtar kelimeye göre IMDB'den filmleri toplar ve bir DataFrame olarak döndürür.

    Argümanlar:
    - weather: Filmleri filtrelemek için kullanılan hava durumu koşulu.
    - keyword: Filmleri aramak için kullanılan anahtar kelime.

    Döndürülen değer:
    - df: Anahtar kelimeye göre IMDB'den toplanan filmlerin bir DataFrame'i.

    Fonksiyon, IMDB web sitesinde belirli bir anahtar kelimeye göre filmleri arar.
    Her film için başlık, tür, derecelendirme, açıklama, yönetmen, oy sayısı ve bütçe bilgilerini toplar.
    Ardından bu verileri bir DataFrame'e dönüştürür ve döndürür.

    Notlar:
    - Anahtar kelime araması IMDB'de arama yapmak için kullanılır.
    - Weather parametresi, filmleri hava durumu koşuluna göre filtrelemek için kullanılabilir.
    """
    titles = []
    genres = []
    ratings = []
    descriptions = []
    directors = []
    votess = []
    grosses = []

    base_url = "https://www.imdb.com/search/keyword/"
    params = {
        "keywords": keyword,
        "sort": "moviemeter,asc",
        "mode": "detail"
    }

    page = 1
    while True:
        params["page"] = page
        response = requests.get(base_url, params=params)
        soup = BeautifulSoup(response.content, "html.parser")
        movie_elements = soup.find_all("div", class_="lister-item mode-detail")

        if not movie_elements:
            break

        for movie_element in movie_elements:
            year_element = movie_element.find("span", class_="lister-item-year text-muted unbold")
            if year_element and ("Video Game" in year_element.text or "TV Series" in year_element.text):
                continue  # Skip video games and TV series
            title_element = movie_element.find("h3", class_="lister-item-header")
            title = title_element.a.text.strip() if title_element else "N/A"
            titles.append(title)

            genre_element = movie_element.find("span", class_="genre")
            genre = genre_element.text.strip() if genre_element else "N/A"
            genres.append(genre)

            rating_element = movie_element.find("div", class_="inline-block ratings-imdb-rating")
            rating = rating_element.strong.text.strip() if rating_element else "N/A"
            ratings.append(rating)

            description_element = movie_element.find("p", class_="")
            description = description_element.text.strip() if description_element else "N/A"
            descriptions.append(description)

            director_element = movie_element.select_one("p.text-muted.text-small a[href^='/name/']")
            director = director_element.text if director_element else "N/A"
            directors.append(director)

            votes_element = movie_element.find("span", attrs={"name": "nv", "data-value": True})
            votes = votes_element["data-value"] if votes_element else "N/A"
            votess.append(votes)

            gross_element = movie_element.find("span", string="Gross:")
            gross = gross_element.find_next_sibling("span").text.strip() if gross_element else "N/A"
            grosses.append(gross)

        page += 1

    data = {
        "Title": titles,
        "Genre": genres,
        "Rating": ratings,
        "Description": descriptions,
        "Director": directors,
        "Votes": votess,
        "Gross": grosses,
        # "Keyword": keyword,
        "Weather": weather,
    }
    df = pd.DataFrame(data)

    return df



keyword_map = {
    "Rain": ["rain", "rainy-day", "rainy-weather", "melancholy", "coziness"],
    "Clear": ["clear-sky", "sun", "sunny", "sunny-day", "sunny-weather", "happiness", "optimism"],
    "Clouds": ["cloud","cloudy-sky", "cloudiness", "serenity", "contemplation"],
    "Drizzle": ["rainfall", "raindrop", "tranquility", "serenity"],
    "Thunderstorm": ["thunderstorm", "storm", "stormy-weather", "awe", "excitement"],
    "Snow": ["snow", "snowing", "winter", "christmas", "wonder", "playfulness", "holiday"],
    "Mist": ["mist", "misty-day", "intrigue", "calmness", "calm"],
    "Fog": ["fog", "foggy-night", "uncertainty", "introspection"]
}



movie_dfs = []
for weather, keywords in keyword_map.items():
    for keyword in keywords:
        movie_dfs.append(scrape_movies_for_keyword(weather, keyword))

all_movies_df = pd.concat(movie_dfs, ignore_index=True)

print(all_movies_df)
all_movies_df.to_csv('imdb_weather_data2.csv')
