import requests
from bs4 import BeautifulSoup


def get_movies():
    url_movies = "https://www.imdb.com/showtimes/cinema/ES/ci17723570/ES/15368"
    response = requests.get(url_movies)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    index = url_movies.find('/', 8)
    base_url = url_movies[:index]

    movie_keys = ['Titulo', 'Estreno', 'Duracion', 'Genero', 'UserRating', 'Rank', 'Horas', 'link']

    list_movies = [
            {
                movie_keys[0]: movie.find("h3").get_text(strip = True)[:-7],
                movie_keys[1]: movie.find("h3").get_text(strip = True)[-6:],
                movie_keys[2]: movie.find(class_ = "cert-runtime-genre").find("time").text,
                movie_keys[3]: movie.find(class_ = "cert-runtime-genre").get_text(strip = True).split("\n")[1],
                movie_keys[4]: ' '.join(movie.find(class_ = "rating_txt").get_text(strip = True).split(" ")[:2]),
                movie_keys[5]: movie.find_all(class_ = "nobr")[-1].get_text(strip = True),
                movie_keys[6]: movie.find(class_="showtimes").get_text(strip = True).split("|"),
                movie_keys[7]: base_url+movie.find(class_="info").find("a").get("href")
            }
            for movie in soup.findAll(True, {'class':['list_item odd', 'list_item even']})
    ]

    resultado = ''
    list_movies_sorted = sorted(list_movies, key=lambda x: float(x['UserRating'].split(":")[1].split("/")[0]), reverse=True)

    top_5_movies = list_movies_sorted[:5]

    for movie_data in top_5_movies:
        formatted_movie = f'''
🎬 *Titulo:* [{movie_data['Titulo']}]({movie_data['link']}) {movie_data['Estreno']}
⌛ *Duracion:* {movie_data['Duracion']}
🌐 *Ranking:* {movie_data['Rank'].split(":")[1]}
🌟 *Valoracion usuarios:* {movie_data['UserRating'].split(":")[1]}
⏰ *Sesiones:* {' | '.join(movie_data['Horas'])}
        '''
        resultado += formatted_movie

    return resultado

