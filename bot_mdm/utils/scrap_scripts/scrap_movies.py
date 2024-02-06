import requests
from bs4 import BeautifulSoup


def get_movies():
    url_movies = "https://www.sensacine.com/cines/cine/E0770/"
    response = requests.get(url_movies)
    soup = BeautifulSoup(response.text, 'html.parser')

    movie_keys = ['title','synopsis', 'image', 'link_ref']

    list_movies = [
        {
            movie_keys[0]: movie.find(class_="meta-title-link").text,
            movie_keys[1]: movie.find(class_="synopsis").text.replace("\n", ""),
            movie_keys[2]: movie.find("img").get("src") if movie.find("img").get("src").startswith("https") else movie.find("img").get("data-src"),
            movie_keys[3]: "https://www.sensacine.com" + movie.find(class_="meta-title-link").get("href")
        }
        for movie in soup.find_all(class_="movie-card-theater")]

    return list_movies

