
import io
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from plottable import ColumnDefinition, Table



def leb_results():
    url_feb = "https://baloncestoenvivo.feb.es/resultados/ligaleboro/1/2023"
    response = requests.get(url_feb)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find(id="_ctl0_MainContentPlaceHolderMaster_jornadaDataGrid")

    match_list = []
    leb_match_keys = ['TEAMS', 'RESULT', 'DATE', 'TIME']

    for fila in table.find_all('tr')[1:]:
        temp_dict = {}

        for key, row in zip(leb_match_keys, fila.find_all(['td', 'th'])):
            temp_dict[key] = row.get_text(strip=True).lower().title()

        match_list.append(temp_dict)



    for i in match_list:
        local, visitor = i['TEAMS'].split("-")
        i['LOCAL'] = local
        i['VISITOR'] = visitor
        i.pop('TEAMS')

    df = pd.DataFrame(match_list)
    df_order = df[['LOCAL', 'RESULT', 'VISITOR', 'DATE', 'TIME']]

    col_defs = (
        [

            ColumnDefinition(
                name="LOCAL",
                textprops={"ha": "center"},
                width=2,
                ),

            ColumnDefinition(
                name="RESULT",
                textprops={"ha": "center"},
                title = "RESULTADO",
                width=0.5,
                ),

            ColumnDefinition(
                name="VISITOR",
                width=2,
                title = "VISITANTE",
                textprops={
                    "ha": "center",}),

            ColumnDefinition(
                name="DATE",
                title = "FECHA",
                textprops={"ha": "center"},
                width=0.7,),

            ColumnDefinition(
                name="TIME",
                title = "HORA",
                textprops={"ha": "center"},
                border="left",
                width=0.35,),

            ])


    fig, ax = plt.subplots(figsize=(12, 6))
    table = Table(
        df_order,
        index_col="LOCAL",
        column_definitions=col_defs,
        row_dividers=True,
        ax=ax,
        row_divider_kw={"linewidth": 1, "linestyle": (0, (1, 5))},
        column_border_kw={"linewidth": 1, "linestyle": "-"})

    image_bytes_io = io.BytesIO()
    plt.savefig(image_bytes_io, 
                format='png', 
                transparent = True, 
                bbox_inches = 'tight')
    image_bytes_io.seek(0)
    plt.close()

    return image_bytes_io



def image(axes_inset, content):
        url = content
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        axes_inset.imshow(img)


def leb_ladder():
    url_feb = "https://www.leboro.es/clasificacion.aspx"
    response = requests.get(url_feb)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    ladder = soup.find("table")

    ladder_list = []

    leb_ladder_keys = ['POSICION', 'EQUIPO', 'PJ', 'PG', 'PP', 'PTS', 'RACHA']

    for row in ladder.find_all('tr')[1:]:
        temp_dict = {}

        cells = row.find_all(['td', 'th'])
        for key, cell in zip(leb_ladder_keys, cells):

            if key == 'PTS':
                temp_dict[key] = cells[7].get_text(strip=True)
            elif key == 'RACHA':
                temp_dict[key] = cells[8].get_text(strip=True)
            else:
                temp_dict[key] = cell.get_text(strip=True)

        ladder_list.append(temp_dict)

        for cell in cells:
            if cell.find(class_="escudo") is not None:
                    temp_dict['IMAGE'] = cell.find(class_="escudo").get("src")


    df = pd.DataFrame(ladder_list)
    df = df[ ['IMAGE'] + [ col for col in df.columns if col != 'IMAGE' ] ]

    col_defs = (
        [

            ColumnDefinition(
                name="IMAGE",
                title="",
                textprops={"ha": "center"},
                width=0.8,
                plot_fn=image
                ),

            ColumnDefinition(
                name="EQUIPO",
                textprops={"ha": "left"},
                width=2,),

            ColumnDefinition(
                name="PTS",
                width=0.35,
                textprops={
                    "ha": "center",}),

            ColumnDefinition(
                name="POSICION",
                textprops={"ha": "center"},
                title = "",
                width=0.35,),

            ColumnDefinition(
                name="PJ",
                textprops={"ha": "center"},
                width=0.35,),

            ColumnDefinition(
                name="PG",
                textprops={"ha": "center"},
                width=0.35,),

            ColumnDefinition(
                name="PP",
                textprops={"ha": "center"},
                width=0.35,),

            ColumnDefinition(
                name="RACHA",
                textprops={"ha": "center"},
                width=0.35,),

            ])

    fig, ax = plt.subplots(figsize=(10, 15))
    table = Table(
        df,
        index_col="POSICION",
        column_definitions=col_defs,
        row_dividers=True,
        ax=ax,
        row_divider_kw={"linewidth": 1, "linestyle": (0, (1, 5))},
        column_border_kw={"linewidth": 1, "linestyle": "-"})

    image_bytes_io = io.BytesIO()
    plt.savefig(image_bytes_io, 
                format = 'png', 
                transparent = True, 
                bbox_inches = 'tight')
    image_bytes_io.seek(0)
    plt.close()

    return image_bytes_io
