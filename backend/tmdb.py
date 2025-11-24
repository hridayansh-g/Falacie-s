#by Hridayansh, Riya, Ishita, Lokendra
import os
import requests
import random
from dotenv import load_dotenv

load_dotenv()
print("TMDB API KEY:", os.getenv("TMDB_API_KEY"))
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

emotion_to_genres = {
    "happy": ["35", "10751"],      # Comedy, Family
    "sad": ["18", "10749"],        # Drama, Romance
    "angry": ["28", "80"],         # Action, Crime
    "surprise": ["9648", "878"],   # Mystery, Sci-Fi
    "fear": ["27", "53"],          # Horror, Thriller
    "disgust": ["99", "18"],       # Documentary, Drama
    "neutral": ["10749", "12"]     # Romance, Adventure
}

def get_movies_by_emotion(emotion):
    genres = emotion_to_genres.get(emotion.lower(), ["18"])
    all_movies = {}

    language_settings = [
        {"language": "en-US", "with_original_language": "en"},  # Hollywood
        {"language": "hi-IN", "with_original_language": "hi"}   # Bollywood
    ]

    for setting in language_settings:
        # 👇 Random page and sort_by every time
        random_page = random.randint(1, 3)
        sort_options = ["popularity.desc", "vote_average.desc", "release_date.desc"]
        sort_by = random.choice(sort_options)

        url = "https://api.themoviedb.org/3/discover/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "with_genres": ",".join(genres),
            "language": setting["language"],
            "with_original_language": setting["with_original_language"],
            "sort_by": sort_by,
            "page": random_page
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            results = response.json().get("results", [])

            random.shuffle(results)  # 🌀 Shuffle results
            for movie in results[:4]:  # 6 random movies from this language
                movie_id = movie.get("id")
                if movie_id not in all_movies:
                    all_movies[movie_id] = {
                        "title": movie.get("title", ""),
                        "overview": movie.get("overview", "No description"),
                        "poster": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get("poster_path") else "",
                        "original_language": movie.get("original_language", "")
                    }

        except Exception as e:
            print(f"Error fetching movies for language {setting['with_original_language']}: {e}")

    # 🧠 Return top 10 from all collected movies
    return list(all_movies.values())[:10]