import requests


def get_api_bicicoruna(target_station):
    station_url = "https://acoruna.publicbikesystem.net/customer/gbfs/v2/en/station_information"
    bike_info = "https://acoruna.publicbikesystem.net/customer/ube/gbfs/v1/en/station_status"

    response_station = requests.get(station_url)
    data_station = response_station.json()

    found_station = None

    for station in data_station["data"]["stations"]:
        if station.get("name").strip().lower() == target_station.lower():
            found_station = station
            break

    if found_station:
        reponse_bike_info = requests.get(bike_info)
        data_bike = reponse_bike_info.json()
        
        for station_bike in data_bike["data"]["stations"]:
            if found_station['station_id'] == station_bike['station_id']:
                message = f"""ℹ️ *Información de la estación:*
                
   - 🚏 *Nombre:* {found_station['name']}
   - 📍 *Dirección:* {found_station['address']}
   - 📬 *Código Postal:* {found_station['post_code']}
                
🚲 *Información de bicicletas:*

   - ➡️ Disponibles: {station_bike['num_bikes_available']}
   - ➡️ Desactivadas: {station_bike['num_bikes_disabled']}
   - ➡️ Normales: {station_bike["num_bikes_available_types"]['mechanical']}
   - ➡️ Eléctricas: {station_bike["num_bikes_available_types"]['ebike']}
                  
🔒 *Docks disponibles:*

   - ➡️ Disponibles: {station_bike['num_docks_available']}
   - ➡️ Desactivados: {station_bike['num_docks_disabled']}"""
                
                return message

    else:
        return (f"No se encontró ninguna estación {target_station}.")


def list_stations():
    station_url = "https://acoruna.publicbikesystem.net/customer/gbfs/v2/en/station_information"

    response_station = requests.get(station_url)
    data_station = response_station.json()
    station_list = [station.get("name").strip() for station in data_station["data"]["stations"]]
    
    message = "🚏 *Lista de Estaciones:*\n"

    for station_name in station_list:
        message += f"- {station_name}\n"
        
    return message
