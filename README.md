# Movie & Song Recommendations by Weather
## Final Project for Miuul Bootcamp

### Purpose of The Project 
**Recommend movies and songs according to instant weather information.**

A study was conducted by extracting data from eight different weather sources via the Open Weather API and by utilizing keywords from the IMDB and Spotify datasets. This study aimed to match the weather information with seasonal patterns found in the IMDB dataset and the Spotify dataset, resulting in movie-song recommendations.


# Project Steps


## Open Weather API
8 different weather information that the user is expected to enter has been determined from the address https://openweathermap.org/api.
We kept this weather information in the weather variable.

- "Clear": The weather is clear and sunny.
- "Clouds": It's cloudy.
- "Rain": It's raining.
- "Drizzle" (Drizzle): Light raindrops are falling.
- "Thunderstorm": There is heavy rain, lightning and thunder.
- "Snow" (Snow): It is snowing.
- "Mist" (Foggy): Foggy weather conditions.
- "Fog" (Dense Fog): Weather conditions with heavy fog.


## Web Scraping

### IMDB
We can search for keywords on IMDB's website. The "Keywords" feature is a feature that allows movies or other content to be associated with specific topics in the IMDb database.
Keywords entered in this section refer to information about the content, theme, subject or other features of the movies.

For example, when you enter a keyword like "rainy weather" or "rainy day", IMDb will associate the relevant movies with the rainy weather or rainy day themes.
This ensures that search results are limited to movies related to these themes. Keywords are used to describe the movie or refer to a particular subject or atmosphere.

We searched for keywords based on 8 weather conditions we pulled from the Open Weather API.

For example, in addition to keywords such as rainy weather for Rain, we also considered words such as melancholy that occurs in people in a rainy weather atmosphere and pulled the data through the BeautifulSoup library.


### Spotify 

On Spotify, we followed a different method. In the method we followed based on “Social Proof”, we handled the most popular playlists related to weather conditions, especially Spotify's official account, and collected the songs under playlists by creating playlists for each weather condition. We shot the playlists we collected using the Spotify API.


## Recommendations 

First, we match/match the weather variable we receive from the user with the movie/song contents that contain the weather information in our own dataset.

Then, using a hybrid approach, we calculate the frequency of words using the TF-IDF method, and recommend a movie/song in decreasing order according to the rating of the movie and according to the Popularity metric for the song.


## Streamlit

We decided to present it to users with an interface using Streamlit. In the recommender.py we created, we called functions that predict movies and songs in Streamlit and used them for each weather condition. We wanted to change the background image specific to each weather condition. We published the site we created on Streamlit.


![streamlit3](https://github.com/recepilyasoglu/Dr.Weather/assets/77547712/e311058c-fc7f-4764-b465-bf226eb52bd7)


![streamlit4](https://github.com/recepilyasoglu/Dr.Weather/assets/77547712/74b35f86-d206-4cfb-83ba-fdfcc21396c2)



## Team Members
- ### Recep İlyasoğlu

<a target="_blank" href="https://www.linkedin.com/in/recepilyasoglu"><img src="https://img.shields.io/badge/-LinkedIn-0077B5?style=for-the-badge&logo=Linkedin&logoColor=white"></img></a>
<a target="_blank" href="https://www.kaggle.com/receplyasolu"><img src="https://img.shields.io/badge/Kaggle-035a7d?style=for-the-badge&logo=kaggle&logoColor=white"></img></a>
<a target="_blank" href="https://github.com/recepilyasoglu"><img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"></img></a>

- ### Dilruba Mermer

<a target="_blank" href="https://www.linkedin.com/in/dilrubamermer"><img src="https://img.shields.io/badge/-LinkedIn-0077B5?style=for-the-badge&logo=Linkedin&logoColor=white"></img></a>
<a target="_blank" href="https://kaggle.com/dilrubamermer"><img src="https://img.shields.io/badge/Kaggle-035a7d?style=for-the-badge&logo=kaggle&logoColor=white"></img></a>
<a target="_blank" href="https://github.com/dilrubamermer"><img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"></img></a>


- ### Özge Çinko

<a target="_blank" href="https://www.linkedin.com/in/ozgecinko"><img src="https://img.shields.io/badge/-LinkedIn-0077B5?style=for-the-badge&logo=Linkedin&logoColor=white"></img></a>
<a target="_blank" href="https://kaggle.com/ozgecinko"><img src="https://img.shields.io/badge/Kaggle-035a7d?style=for-the-badge&logo=kaggle&logoColor=white"></img></a>
<a target="_blank" href="https://github.com/ozgecinko"><img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"></img></a>

- ### Sami Özen

<a target="_blank" href="https://www.linkedin.com/in/mahmutsamiozen"><img src="https://img.shields.io/badge/-LinkedIn-0077B5?style=for-the-badge&logo=Linkedin&logoColor=white"></img></a>
<a target="_blank" href="https://kaggle.com/samiozen"><img src="https://img.shields.io/badge/Kaggle-035a7d?style=for-the-badge&logo=kaggle&logoColor=white"></img></a>
<a target="_blank" href="https://github.com/samiozenn"><img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"></img></a>



