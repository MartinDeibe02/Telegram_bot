import pandas as pd
from io import StringIO


def convert_file(ruta, conversion):
    try:
        if conversion == 'csv_to_json':
            df = pd.read_csv(ruta, encoding='ISO-8859-1')
            json_data = df.to_json(orient='records')

            json_filename = 'data.json'
            with open(json_filename, 'w') as json_file:
                json_file.write(json_data)

            data = open(json_filename, 'rb')

        elif conversion == 'json_to_csv':
            with open(ruta, 'r') as json_file:
                json_data = json_file.read()

            json_io = StringIO(json_data)

            df = pd.read_json(json_io, orient='records')

            csv_filename = 'data.csv'
            df.to_csv(csv_filename, index=False)

            data = open(csv_filename, 'rb')


        return data

    except Exception as e:
        return None