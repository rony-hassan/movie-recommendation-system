import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=90d0f092602a737f3c4aea7f6554c9df&language=en-US'.format(movie_id))
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500' + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')
selected_movie_name = st.selectbox('Pick a movie you watched',
             movies['title'].values)

if st.button('Recommend Next Movie'):
    names,posters = recommend(selected_movie_name)

    st.markdown("""
        <style>
        .movie-name {
            height: 80px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True)

    cols = st.columns(5)

    for j, col in enumerate(cols):
        with col:
            st.markdown(f'<div class="movie-name">{names[j]}</div>', unsafe_allow_html=True)
            st.image(posters[j])