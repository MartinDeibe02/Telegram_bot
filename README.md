# Ejecución de bot de Telegram

Aqui estarán las instrucciones sobre cómo ejecutar el contenedor Docker para el bot de telegran en la consola y a través de Docker Desktop. Asegúrate de tener Docker instalado en tu sistema antes de comenzar.

## Ejecución desde la Consola

1. Abre la consola de comandos en tu sistema.

2. Utiliza el siguiente comando para ejecutar el contenedor Docker:

    ```bash
    docker run --rm -e BOT_TOKEN=token_bot_telegram -e WEATHER_TOKEN=token_openweather -e NASA_TOKEN=token_api_nasa nombre_imagen
    ```

   Asegúrate de reemplazar `BOT_TOKEN`, `WEATHER_TOKEN`, `NASA_TOKEN` con el token que corresponde a cada uno.
   
    - **BOT_TOKEN**: Tu token de bot de telegram (puedes obtenerlo de [BotFather](https://telegram.me/BotFather)).
   - **WEATHER_TOKEN**: Tu token de OpenWeather (puedes obtenerlo de [OpenWeather](https://openweathermap.org/api)).
   - **NASA_TOKEN**: Tu token de NASA (puedes obtenerlo en la [página de APIs de la NASA](https://api.nasa.gov/)).


3. El contenedor se ejecutará con la configuración proporcionada.

## Ejecución desde Docker Desktop

1. Abre Docker Desktop en tu sistema.

2. En el menú, selecciona "Images" para asegurarte de que la imagen del contenedor está disponible. Si no está presente, puedes descargarla buscando `martindeibe02/telegram_bot`

3. Dirígete a la sección "Containers" y haz clic en "Run" o "Create" para crear un nuevo contenedor.

4. Configura las variables de entorno:

   - **BOT_TOKEN**: Tu token de bot.
   - **WEATHER_TOKEN**: Tu token de Weather.
   - **NASA_TOKEN**: Tu token de NASA.

5. Guarda la configuración y haz clic en "Run" para iniciar el contenedor.

6. Verifica la consola de salida para asegurarte de que el contenedor se está ejecutando correctamente.


## Comandos del Bot

El bot responderá a los siguientes comandos:

### API
- `/meteo`: Este comando preguntará al usuario por una ciudad y mostrará el tiempo de la ciudad dada
- `/apod`: Este comando devolverá la imagen del día de la nasa junto a su descripción
- `/joke`: Este comando devolverá un chiste aleatorio
- `/bicicoruna`: Este comando dará dos opciones:
    - **Consultar parada**: Devolverá la información sobre la parada seleccionada.
   - **Listar paradas**: Devolverá una lista de todas las paradas.
### SCRAPPING

- `/noticias`: Este comando devolverá un listado con 5 noticias sacadas de [La voz de Galicia](https://www.lavozdegalicia.es/)
- `/cartelera`: Este comando devolverá un listado de 5 peliculas de la cartelera de [Cinesa](https://www.imdb.com/showtimes/cinema/ES/ci17723570/ES/15368)
- `/leb`: Este comando nos dará dos opciones:
   - **Clasificación**: Devolverá una foto(gráfico) con la clasificación actual de la LebOro 
   - **Listar paradas**: Devolverá una foto(gráfico) con los partidos de la semana

### FICHEROS
- Si pasamos al bot un fichero csv, nos devolverá un fichero json con la misma informacion y viceversa. Ademas de esto nos mostrara un mensaje de información del contenido del fichero.

### BASE DE DATOS
- `/infierno`: Al ejecutar este codigo se le pedira al usuario que introduzca un nombre, posteriormente se hará una consulta a la base de datos y mostrará en que nivel del infierno esta.
