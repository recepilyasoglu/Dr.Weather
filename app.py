from io import BytesIO

import requests
import streamlit as st
import pandas as pd
from PIL.Image import Image

from recommender import get_weather, get_songs_by_weather, get_movies_by_weather


weather_images = {
    "Clear": "https://images.pexels.com/photos/281260/pexels-photo-281260.jpeg",
    "Clouds": "https://images.pexels.com/photos/531756/pexels-photo-531756.jpeg",
    "Rain": "https://images.pexels.com/photos/1529360/pexels-photo-1529360.jpeg",
    "Drizzle": "https://images.pexels.com/photos/7002970/pexels-photo-7002970.jpeg",
    "Thunderstorm": "https://images.pexels.com/photos/1118869/pexels-photo-1118869.jpeg",
    "Snow": "https://images.pexels.com/photos/1710352/pexels-photo-1710352.jpeg",
    "Mist": "https://images.pexels.com/photos/691668/pexels-photo-691668.jpeg",
    "Fog": "https://images.pexels.com/photos/1287075/pexels-photo-1287075.jpeg",
}


def main():
    st.title("DOCTOR WEATHER")
    st.subheader("Best song and movie recommendations!")

    city = st.text_input("Enter your city name:")

    if st.button("Get Recommendations"):
        if city:
            weather = get_weather(city)
            if weather:
                background_image = weather_images.get(weather)
                if background_image:
                    st.markdown(
                        f"""
                        <style>
                        [data-testid="stAppViewContainer"]{{
                            background: url('{background_image}');
                            background-size: cover;
                        }}
                        
                        div.css-ocqkz7.e1tzin5v3 {{
                            background-color: white;
                            border: 2px solid #CCCCCC;
                            padding: 5% 5% 5% 10%;
                            border-radius: 5px;
                            color: black;
                            text-align: center;
                            display: flex;
                        }}
                        </style>
                        """,
                        unsafe_allow_html=True
                    )
                st.subheader(f"Recommendations for {city} city in {weather} Weather")

                container = st.container()
                with container:
                    st.subheader(f"Recommended Movies")
                    recommended_movies = get_movies_by_weather("Weather", "Description", weather, 3)
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(recommended_movies.loc[0, "Title"])
                        st.write(recommended_movies.loc[0, "Genre"])
                        st.write(recommended_movies.loc[0, "Rating"])
                        st.write(recommended_movies.loc[0, "Description"])

                    with col2:
                        st.write(recommended_movies.loc[1, "Title"])
                        st.write(recommended_movies.loc[1, "Genre"])
                        st.write(recommended_movies.loc[1, "Rating"])
                        st.write(recommended_movies.loc[1, "Description"])

                    with col3:
                        st.write(recommended_movies.loc[2, "Title"])
                        st.write(recommended_movies.loc[2, "Genre"])
                        st.write(recommended_movies.loc[2, "Rating"])
                        st.write(recommended_movies.loc[2, "Description"])

                with container:
                    st.subheader(f"Recommended Songs")
                    recommended_songs = get_songs_by_weather("Weather", "Track Name", weather, 3)
                    # st.dataframe(recommended_songs)
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(recommended_songs.loc[0, "Track Name"])
                        st.image(recommended_songs.loc[0, "Image"], use_column_width=True)
                        st.write(recommended_songs.loc[0, "Album"])

                    with col2:
                        st.write(recommended_songs.loc[1, "Track Name"])
                        st.image(recommended_songs.loc[1, "Image"], use_column_width=True)
                        st.write(recommended_songs.loc[1, "Album"])

                    with col3:
                        st.write(recommended_songs.loc[2, "Track Name"])
                        st.image(recommended_songs.loc[2, "Image"], use_column_width=True)
                        st.write(recommended_songs.loc[2, "Album"])

            else:
                st.error("Failed to fetch weather information. Please check the city name.")
        else:
            st.warning("Please enter a city name.")


if __name__ == "__main__":
    main()
