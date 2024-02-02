import requests
from bs4 import BeautifulSoup

def leb_results():
    url_feb = "https://baloncestoenvivo.feb.es/resultados/ligaleboro/1/2023"
    response = requests.get(url_feb)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find(id="_ctl0_MainContentPlaceHolderMaster_jornadaDataGrid")

    match_list = []
    leb_match_keys = ['teams', 'result', 'date', 'time']

    # Iterar filas ignorando la primera
    for fila in table.find_all('tr')[1:]:
        temp_dict = {}
        
        for key, row in zip(leb_match_keys, fila.find_all(['td', 'th'])):
            temp_dict[key] = row.get_text(strip=True).lower().title()
        
        match_list.append(temp_dict)

    telegram_message = ""
    for match in match_list:
        telegram_message += f"*Equipos:* {match['teams']}\n"
        telegram_message += f"*Resultado:* {match['result']}\n"
        telegram_message += f"*Fecha:* {match['date']} {match['time']}\n\n"
    return telegram_message


def leb_ladder(soup):
    url_feb = "https://baloncestoenvivo.feb.es/resultados/ligaleboro/1/2023"
    response = requests.get(url_feb)
    soup = BeautifulSoup(response.text, 'html.parser')
    ladder = soup.find(id="_ctl0_MainContentPlaceHolderMaster_clasificacionDataGrid")

    ladder_list = []

    leb_ladder_keys = ['position', 'team', 'matches_played', 'matches_w', 'matches_l', 'points']

    for row in ladder.find_all('tr')[1:]:
        temp_dict = {}

        cells = row.find_all(['td', 'th'])
        for key, cell in zip(leb_ladder_keys, cells):
            if key == 'points':
                temp_dict[key] = cells[7].get_text(strip=True) 
            else:
                temp_dict[key] = cell.get_text(strip=True)

        ladder_list.append(temp_dict)

    ladder_list
