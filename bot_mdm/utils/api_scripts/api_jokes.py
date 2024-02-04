import requests

def get_api_joke():
    url_jokes = "https://v2.jokeapi.dev/joke/Any"
    payload = {"format": "json", 'type':'single', 'lang':'es'}
    response = requests.get(url_jokes , params=payload)
    joke = response.json()['joke'].strip().replace("'", "").replace('\n', "")
    return f"🤣{joke}🤣"