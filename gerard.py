import json
import matplotlib.pyplot as plt
from plots import *

from datetime import datetime

def loaders(): 
    # Ruta al archivo JSON
    json_file_scheduler = 'schedule.json'
    json_file_record = '06_53_16.JSON'

    # Cargar los datos del archivo JSON
    with open(json_file_scheduler) as file:
        scheduler = json.load(file)

    with open(json_file_record) as file:
        test1 = json.load(file)

    return scheduler, test1

def get_first_station(scheduler, linea, sentido, origen, t_inicio):
    # seleccionar los "departure_time" de la linea y sentido seleccionados
    departure_times = []
    for item in scheduler:
        if item['route_short_name'] == linea and item['trip_headsign'] == sentido and item['stop_name'] == origen:
            try:
                time = datetime.strptime(item['departure_time'], "%H:%M:%S").time()
                departure_times.append(time)
            except ValueError:
                continue
    # Convertir t_inicio a datetime para poder hacer la comparación
    t_inicio = datetime.combine(datetime.today(), t_inicio)

    # Calcular la hora más cercana
    nearest_time = min(departure_times, key=lambda x: abs(datetime.combine(datetime.today(), x) - t_inicio))

    return nearest_time

def get_stop_ids_from_time(scheduler, linea, origen, sentido, timestamp):
    stop_ids = []

    for item in scheduler:
        if item['route_short_name'] == linea and item['trip_headsign'] == sentido and item['stop_name'] == origen:
            try:
                departure_time = datetime.strptime(item['departure_time'], "%H:%M:%S").time()
                if departure_time >= timestamp:
                    stop_ids.append(item)
            except ValueError:
                continue
    
    return stop_ids

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

def get_closest_time_vector(vectors, target_time):
    def time_difference(vector):
        time_str = vector["departure_time"]  # Assuming the time is in the third position
        vector_time = datetime.strptime(time_str, "%H:%M:%S").time()
        return abs(datetime.combine(datetime.today(), vector_time) - datetime.combine(datetime.today(), target_time))
    
    closest_vector = min(vectors, key=time_difference)
    
    return closest_vector

def print_connection_by_timestamp(data, timestamp):
    for item in data:
        if item[0]['time'] == timestamp:
            print(f"Connection at timestamp {timestamp}: {item['connection']}")
            return
    print(f"No connection found for timestamp {timestamp}")


def __main__():
    scheduler, travel = loaders()
    linea = travel['options']['linea']
    sentido = travel['options']['direccion']
    origen = travel['options']['origen']
    destino = travel['options']['destino']
    t_inicio = datetime.strptime(travel['data'][0]['time'], "%H:%M:%S").time()

    stations = get_stations(scheduler, origen, destino, sentido, linea, t_inicio)
    t_inicio = get_first_station(scheduler, linea, sentido, origen, t_inicio)
    print("Hora de salida del tren:", t_inicio.strftime("%H:%M:%S")) # Hora a la que sale el tren
    
    llista_trajecte = [[t_inicio.strftime("%H:%M:%S"), origen]]

    for i in range(len(stations)-1):
        actual = stations[i+1]
        llista_retallada = get_stop_ids_from_time(scheduler, linea, actual, sentido, t_inicio)
        closest_vector = get_closest_time_vector(llista_retallada, t_inicio)
        t_inicio = datetime.strptime(closest_vector["departure_time"], "%H:%M:%S").time()
        origen = closest_vector["stop_name"]
        llista_trajecte.append([t_inicio.strftime("%H:%M:%S"), origen])

    print("Lista de trayecto:", llista_trajecte) 
    
    values_list = [[entry['connection']] for entry in travel]
    time_list = [[entry['time']] for entry in travel]
    times_datetime = [datetime.strptime(time[0], "%H:%M:%S") for time in time_list]

    # Crear el gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(times_datetime, values_list, marker='o', linestyle='-')

    # Configurar etiquetas y título
    plt.xlabel('Tiempo')
    plt.ylabel('Valor')
    plt.title('Valores en el Tiempo')

    # Rotar las etiquetas del eje x para mayor legibilidad
    plt.xticks(rotation=45)

    # Mostrar el gráfico
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    __main__()
