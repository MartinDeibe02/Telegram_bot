import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
import io


def get_html_content():
    url_feb = "https://baloncestoenvivo.feb.es/resultados/ligaleboro/1/2023"
    response = requests.get(url_feb)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def leb_results():
    soup = get_html_content()

    table = soup.find(id="_ctl0_MainContentPlaceHolderMaster_jornadaDataGrid")

    match_list = []
    leb_match_keys = ['TEAMS', 'RESULT', 'DATE', 'TIME']

    for fila in table.find_all('tr')[1:]:
        temp_dict = {}
        
        for key, row in zip(leb_match_keys, fila.find_all(['td', 'th'])):
            temp_dict[key] = row.get_text(strip=True).lower().title()
        
        match_list.append(temp_dict)

    df = pd.DataFrame(match_list)
    fig, ax = plt.subplots(figsize = (8, 1))

    ax.axis('off')
    colors = ['lightgray', 'white']
    cell_colors = [[colors[i % 2] for _ in range(len(df.columns))] for i in range(len(df))]
    
    col_widths = [0.5, 0.1, 0.1, 0.1]

    ax.table(cellText = df.values, 
             colLabels = df.columns, 
             cellLoc = 'center', 
             loc = 'center',
             cellColours = cell_colors, 
             colWidths = col_widths)
    fig.set_size_inches(10, 2)

    image_bytes_io = io.BytesIO()
    plt.savefig(image_bytes_io, 
                format='png', 
                transparent = True, 
                bbox_inches = 'tight')
    image_bytes_io.seek(0)
    plt.close()

    return image_bytes_io


def leb_ladder():
    soup = get_html_content()
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


    fig, ax = plt.subplots(figsize = (11, 3))
    ax.axis('off')

    col_widths = [0.1, 0.4, 0.2, 0.2, 0.2, 0.2]
    colors = ['lightgray', 'white']
    cell_colors = [[colors[i % 2] for _ in range(len(df.columns))] for i in range(len(df))]
    
    ax.table(cellText = df.values, 
             colLabels = df.columns, 
             cellLoc = 'center', 
             loc = 'center', 
             colWidths = col_widths, 
             cellColours = cell_colors)

    fig.set_size_inches(12, 6)

    image_bytes_io = io.BytesIO()
    plt.savefig(image_bytes_io, 
                format = 'png', 
                transparent = True, 
                bbox_inches = 'tight')
    image_bytes_io.seek(0)
    plt.close()

    return image_bytes_io
