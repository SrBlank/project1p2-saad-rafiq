import json
import os
import requests
import flask
import random
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

"""Comment either create_movie_poster_url or comment the two lines after"""
#create_movie_poster_base_url()
global movie_base_poster_url
movie_base_poster_url = "https://image.tmdb.org/t/p/w500"

def get_movie_information_by_id(id):
    TMDB_GET_MOVIE_DETAILS_ID_BASE_URL = "https://api.themoviedb.org/3/movie/" + str(id)
    movie_details_response = requests.get(
        TMDB_GET_MOVIE_DETAILS_ID_BASE_URL,
        params={
            'api_key': os.getenv('TMDB_API_KEY')
        }   
    )
    
    movie_raw_data_json = movie_details_response.json()

    global movie_original_title 
    global movie_tagline
    global movie_desc
    global movie_built_poster_url
    global movie_genres

    movie_original_title = movie_raw_data_json['original_title']
    movie_tagline = movie_raw_data_json['tagline']
    movie_desc = movie_raw_data_json['overview']
    movie_built_poster_url = movie_base_poster_url + movie_raw_data_json['poster_path']
    movie_genres = ""

    for genre in range(0,len(movie_raw_data_json['genres'])):
        movie_genres += movie_raw_data_json['genres'][genre]['name']
        if genre != (len(movie_raw_data_json['genres'])-1):
            movie_genres += ", "

def create_movie_poster_base_url():
    TMDB_CONFIGURATION_BASE_URL = "https://api.themoviedb.org/3/configuration"
    configuration_response = requests.get(
        TMDB_CONFIGURATION_BASE_URL,
        params={
            'api_key': os.getenv('TMDB_API_KEY')
        }   
    )

    global movie_base_poster_url
    movie_base_poster_url = configuration_response.json()['images']['secure_base_url'] + configuration_response.json()['images']['poster_sizes'][4]

def get_movie_wiki_link(movie_title):
    MEDIA_WIKI_BASE_URL = "https://en.wikipedia.org/w/api.php"
    response = requests.get(
        MEDIA_WIKI_BASE_URL,
        params={
            "action": "opensearch",
            "namespace": "0",
            "search": str(movie_title),
            "limit": "10",
            "format": "json"
        }
    )

    wiki_raw_data_json = response.json()
    wiki_article_links = wiki_raw_data_json[3]

    article_index = 0
    for i in range(0, len(wiki_article_links)):
        if(wiki_article_links[i].find("film") != -1):
            article_index = i

    return wiki_article_links[article_index]