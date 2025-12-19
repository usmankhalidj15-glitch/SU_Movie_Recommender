import requests
import re, os
from typing import Optional, List, Dict
from dotenv import load_dotenv
load_dotenv() 
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
TMDB_BASE_URL = "https://api.themoviedb.org/3/search/movie"

def get_movie_poster_url(movie_title: str) -> Optional[str]:
    cleaned_title = re.sub(r'\s*\(\d{4}\)$', '', movie_title).strip()
    query_title = cleaned_title if cleaned_title else movie_title

    params = {
        "api_key": TMDB_API_KEY,
        "query": query_title,
        "language": "en-US"
    }

    try:
        response = requests.get(TMDB_BASE_URL, params=params)
        
        response.raise_for_status() 
        data = response.json()

        if data.get("results"):
            for result in data["results"]:
                if result.get("poster_path"):
                    return f"{TMDB_IMAGE_BASE_URL}{result['poster_path']}"
        
        return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from TMDB for '{movie_title}': {e}")
        return None

def fetch_posters_for_movies(movie_list: List[str]) -> Dict[str, Optional[str]]:
    
    poster_urls = {}
    for movie in movie_list:
        poster_urls[movie] = get_movie_poster_url(movie)
    return poster_urls