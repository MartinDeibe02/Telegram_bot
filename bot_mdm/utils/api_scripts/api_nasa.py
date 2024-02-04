def get_api_apod():
    url_nasa = "https://api.nasa.gov/planetary/apod"
    payload = {"api_key": "token"}
    response = requests.get(url_nasa, params=payload)
    url_apod, desc_apod, title = response.json()['hdurl'], response.json()['explanation'], response.json()['title']

    return f"*{title}*", desc_apod, url_apod