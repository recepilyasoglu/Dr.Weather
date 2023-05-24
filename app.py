import requests
import streamlit as st
import pandas as pd
from PIL.Image import Image

from recommender import get_weather, get_songs_by_weather, get_movies_by_weather

weather_images = {
    "Clear": "https://images.pexels.com/photos/1647177/pexels-photo-1647177.jpeg",
    "Clouds": "https://images.pexels.com/photos/531756/pexels-photo-531756.jpeg",
    "Rain": "https://images.pexels.com/photos/1529360/pexels-photo-1529360.jpeg",
    "Drizzle": "https://images.pexels.com/photos/7002970/pexels-photo-7002970.jpeg",
    "Thunderstorm": "https://images.pexels.com/photos/1118869/pexels-photo-1118869.jpeg",
    "Snow": "https://images.pexels.com/photos/1710352/pexels-photo-1710352.jpeg",
    "Mist": "https://images.pexels.com/photos/691668/pexels-photo-691668.jpeg",
    "Fog": "https://images.pexels.com/photos/1287075/pexels-photo-1287075.jpeg",
}

weather_colors = {
    "Clear": "#E6F4F1",
    "Clouds": "#FFFFFF",
    "Rain": "#D8E6ED",
    "Drizzle": "#FAF8FF",  # Teal
    "Thunderstorm": "#FEFAE6",  # Mor
    "Snow": "#F3FAFF",  # Beyaz
    "Mist": "#FAF7FF",  # Gümüş
    "Fog": "#F4F9FF",  # Koyu Gümüş
}


# Footer element
def footer(background_color=""):
    st.markdown(
        f"""
        <style>
        .footer {{
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            padding: 10px;
            text-align: center;
            background-color: {background_color};
        }}
        
        .grid-container {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 10px;
        }}
        .grid-item {{
            text-align: center;
        }}
        .name {{
            color: white;
            font-weight: bold;
            margin-bottom: 5px;
            text-shadow: black 0.1em 0.1em 0.1em;
        }}
        .links {{
            display: flex;
            justify-content: center;
            margin-top: 5px;
        }}
        .links a {{
            color: white;
            margin: 0 5px;
        }}
        .links a:visited {{color: #d3f2ef}} 
        .links a:hover {{color: #bcaedf}}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="footer">
            <div class="grid-container">
                <div class="grid-item">
                    <div class="name">Recep İlyasoğlu</div>
                    <div class="links">
                        <a href="https://github.com/recepilyasoglu" target="_blank">GitHub</a>
                        <a href="https://linkedin.com/in/recepilyasoglu" target="_blank">LinkedIn</a>
                        <a href="https://kaggle.com/receplyasolu" target="_blank">Kaggle</a>
                    </div>
                </div>
                <div class="grid-item">
                    <div class="name">Dilruba Mermer</div>
                    <div class="links">
                        <a href="https://github.com/dilrubamermer" target="_blank">GitHub</a>
                        <a href="https://linkedin.com/in/dilrubamermer" target="_blank">LinkedIn</a>
                        <a href="https://kaggle.com/dilrubamermer" target="_blank">Kaggle</a>
                    </div>
                </div>
                <div class="grid-item">
                    <div class="name">Özge Çinko</div>
                    <div class="links">
                        <a href="https://github.com/ozgecinko" target="_blank">GitHub</a>
                        <a href="https://linkedin.com/in/ozgecinko" target="_blank">LinkedIn</a>
                        <a href="https://kaggle.com/in/ozgecinko" target="_blank">Kaggle</a>
                    </div>
                </div>
                <div class="grid-item">
                    <div class="name">Sami Özen</div>
                    <div class="links">
                        <a href="https://github.com/samiozenn" target="_blank">GitHub</a>
                        <a href="https://linkedin.com/in/mahmutsamiozen" target="_blank">LinkedIn</a>
                        <a href="https://kaggle.com/samiozen" target="_blank">Kaggle</a>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def body_style():
    st.markdown(
        f"""
        <style>
        #MainMenu, header, footer {{
            visibility: hidden;
        }}
        body {{
            background-color: #d3f2ef;
            font-family: 'Source Sans Pro', sans-serif !important;
        }}
        h1 {{
            color: white;
            text-shadow: black 0.2em 0.2em 0.2em;
        }}
        label {{
            color: white;
            text-shadow: black 0.2em 0.2em 0.2em;
        }}

        img {{
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 50%;
        }}

        .css-ffhzg2 {{
            background: rgb(37,29,57);
            background: -moz-radial-gradient(circle, rgba(37,29,57,1) 0%, rgba(44,45,69,1) 29%, rgba(57,74,90,1) 65%, rgba(76,118,123,1) 95%, rgba(76,118,123,1) 100%, rgba(96,165,158,1) 100%);
            background: -webkit-radial-gradient(circle, rgba(37,29,57,1) 0%, rgba(44,45,69,1) 29%, rgba(57,74,90,1) 65%, rgba(76,118,123,1) 95%, rgba(76,118,123,1) 100%, rgba(96,165,158,1) 100%);
            background: radial-gradient(circle, rgba(37,29,57,1) 0%, rgba(44,45,69,1) 29%, rgba(57,74,90,1) 65%, rgba(76,118,123,1) 95%, rgba(76,118,123,1) 100%, rgba(96,165,158,1) 100%);
            filter: progid:DXImageTransform.Microsoft.gradient(startColorstr="#251d39",endColorstr="#60a59e",GradientType=1);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def main():

    body_style()
    st.title("DR. WEATHER")
    st.subheader("Discover the perfect harmony of tunes and movies!")
    city = st.text_input("Enter your city name:")
    if st.button("Get Recommendations"):
        if city:
            weather = get_weather(city)
            if weather:
                background_image = weather_images.get(weather)
                weather_color = weather_colors.get(weather)
                if background_image:
                    st.markdown(
                        f"""
                        <style>
                        h3 {{
                            color: white;
                            text-shadow: black 0.2em 0.2em 0.2em;
                        }}
                        
                        [data-testid="stAppViewContainer"]{{
                            background: url('{background_image}');
                            background-size: cover;
                        }}
                        
                        div.css-ocqkz7.e1tzin5v3 {{
                            background-color: {weather_color};
                            border: 2px solid #CCCCCC;
                            padding: 5% 5% 5% 10%;
                            border-radius: 5px;
                            color: black;
                            text-align: center;
                            display: flex;
                            box-shadow: 0 3px 10px rgb(0 0 0 / 0.2);
                        }}
                        </style>
                        """,
                        unsafe_allow_html=True
                    )
                st.subheader(f"Recommendations for {city} city in {weather}")
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
    else:
        left_co, cent_co, last_co = st.columns(3)
        with cent_co:
            st.image("assets/drWeather.png")
        footer()


if __name__ == "__main__":
    main()
