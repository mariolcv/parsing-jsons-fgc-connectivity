import json
from datetime import datetime


def loaders(): 
    # Ruta al archivo JSON
    json_file_scheduler = 'C:/hack_uab/parsing-jsons-fgc-connectivity/schedule.json'
    json_file_record = 'C:/hack_uab/parsing-jsons-fgc-connectivity/test.json'

    # Cargar los datos del archivo JSON
    with open(json_file_scheduler) as file:
        scheduler = json.load(file)

    with open(json_file_record) as file:
        test1 = json.load(file)

    return scheduler, test1


def get_first_station(scheduler, linea, sentido, origen, t_inicio):
     # seleccionar los "departure_time" de la linea y sentido seleccionados
    departure_time = []
    for item in scheduler:
        if item['route_short_name'] == linea and item['trip_headsign'] == sentido and item['stop_name'] == origen:
            try:
                time = datetime.strptime(item['departure_time'], "%H:%M:%S").time()
                departure_time.append(time)
            except ValueError:
                continue
    # Convertir t_inicio a datetime para poder hacer la comparación
    t_inicio = datetime.combine(datetime.today(), t_inicio)

    # Calcular la hora más cercana
    nearest_time = min(departure_time, key=lambda x: abs(datetime.combine(datetime.today(), x) - t_inicio))

    return nearest_time

def get_stations(scheduler, origen, destino, sentido, linea, t_inicio):
    # seleccionar los valores únicos de "stop_name" de la linea y sentido seleccionados
    
    stops = {}
    for item in scheduler:
        if item['route_short_name'] == linea and item['trip_headsign'] == sentido:
            if item['stop_name'] not in stops.keys():
                stops[item['stop_name']] = item['stop_sequence']
    # ordenar por "stop_sequence"
    stations = sorted(stops, key=stops.get)
    # eliminar las estaciones antes de la estación de origen
    stations = stations[stations.index(origen):stations.index(destino)+1]
    return stations

def __main__():
    scheduler, travel = loaders()

     # asignar datos principales
    linea = travel['options']['linea']
    sentido = travel['options']['final_linea']
    origen = travel['options']['origen']
    destino = travel['options']['destino']
    t_inicio = datetime.strptime(travel['data'][0]['time'], "%H:%M:%S").time()


    t_inicio = get_first_station(scheduler, linea, sentido, origen, t_inicio)
    stations = get_stations(scheduler, origen, destino, sentido, linea, t_inicio)
    print(stations)


if __name__ == "__main__":
    __main__()