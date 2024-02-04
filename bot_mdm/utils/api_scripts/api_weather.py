import datetime
import requests

def get_weather(city):
    url_openweather = "https://api.openweathermap.org/data/2.5/weather"
    payload = {'q':city, 'appid': 'token','units': 'metric', 'lang':'es'}
    response = requests.get(url_openweather, params=payload)

    if response.status_code == 200:

        weather_data = response.json()['main']
        weather_description = response.json()['weather'][0]['description']
        sys_data = response.json()['sys']

        temp, temp_max, temp_min, temp_feel, humidity = weather_data['temp'], weather_data['temp_max'], weather_data['temp_min'], weather_data['feels_like'], weather_data['humidity']
        sunset, sunrise = datetime.datetime.fromtimestamp(sys_data['sunset']), datetime.datetime.fromtimestamp(sys_data['sunrise'])
        
        weather_info = f"""
    ☁️ Clima en {city}:
        - Temperatura: {temp}°C 🌡️
        - Temperatura Máxima: {temp_max}°C 🔥
        - Temperatura Mínima: {temp_min}°C ❄️
        - Sensación Térmica: {temp_feel}°C 🌡️
        - Humedad: {humidity}% 💦
        - Descripción: {weather_description.capitalize()} ☁️
        - Atardecer: {sunset.strftime('%H:%M:%S')} 🌅
        - Amanecer: {sunrise.strftime('%H:%M:%S')} 🌄
    """
        return weather_info
    else:
        return f'No se ha encontrado {city}'