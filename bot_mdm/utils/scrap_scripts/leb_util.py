import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
import io


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


def leb_ladder():
    url_feb = "https://baloncestoenvivo.feb.es/resultados/ligaleboro/1/2023"
    response = requests.get(url_feb)
    soup = BeautifulSoup(response.text, 'html.parser')
    ladder = soup.find(id="_ctl0_MainContentPlaceHolderMaster_clasificacionDataGrid")

    ladder_list = []

    leb_ladder_keys = ['POSITION', 'TEAMS', 'MATCHES_PLAYED', 'MATCHES_W', 'MATCHES_L', 'POINTS']

    for row in ladder.find_all('tr')[1:]:
        temp_dict = {}

        cells = row.find_all(['td', 'th'])
        for key, cell in zip(leb_ladder_keys, cells):
            if key == 'POINTS':
                temp_dict[key] = cells[7].get_text(strip=True) 
            else:
                temp_dict[key] = cell.get_text(strip=True)

        ladder_list.append(temp_dict)

    df = pd.DataFrame(ladder_list)

    fig, ax = plt.subplots(figsize=(11, 4))
    ax.axis('off')

    col_widths = [0.1, 0.4, 0.2, 0.2, 0.2, 0.2]

    ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center', colWidths=col_widths)

    image_bytes_io = io.BytesIO()
    plt.savefig(image_bytes_io, format='png', transparent=True)
    image_bytes_io.seek(0)

    plt.close()

    return image_bytes_io
