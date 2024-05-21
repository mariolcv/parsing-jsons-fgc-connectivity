import json
import matplotlib.pyplot as plt
from datetime import datetime

def loaders(): 
    # Cargar los datos del archivo JSON
    json_file_scheduler = 'schedule.json'
    json_file_record = '08_31_01.JSON'

    with open(json_file_scheduler) as file:
        scheduler = json.load(file)

    with open(json_file_record) as file:
        test1 = json.load(file)

    return scheduler, test1

def get_first_station(scheduler, linea, sentido, origen, t_inicio):
    departure_times = []
    for item in scheduler:
        if item['route_short_name'] == linea and item['trip_headsign'] == sentido and item['stop_name'] == origen:
            try:
                time = datetime.strptime(item['departure_time'], "%H:%M:%S").time()
                departure_times.append(time)
            except ValueError:
                continue
    
    t_inicio = datetime.combine(datetime.today(), t_inicio)
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
    stops = {}
    for item in scheduler:
        if item['route_short_name'] == linea and item['trip_headsign'] == sentido:
            if item['stop_name'] not in stops.keys():
                stops[item['stop_name']] = item['stop_sequence']

    stations = sorted(stops, key=stops.get)
    stations = stations[stations.index(origen):stations.index(destino)+1]
    return stations

def get_closest_time_vector(vectors, target_time):
    def time_difference(vector):
        time_str = vector["departure_time"]
        vector_time = datetime.strptime(time_str, "%H:%M:%S").time()
        return abs(datetime.combine(datetime.today(), vector_time) - datetime.combine(datetime.today(), target_time))
    
    closest_vector = min(vectors, key=time_difference)
    
    return closest_vector

def __main__():
    scheduler, travel = loaders()
    linea = travel['options']['linea']
    sentido = travel['options']['direccion']
    origen = travel['options']['origen']
    destino = travel['options']['destino']
    t_inicio = datetime.strptime(travel['data'][0]['time'], "%H:%M:%S").time()

    stations = get_stations(scheduler, origen, destino, sentido, linea, t_inicio)
    t_inicio = get_first_station(scheduler, linea, sentido, origen, t_inicio)
    #t_inicio = datetime.strptime("08:32:28", "%H:%M:%S").time()    # en caso de error por tiempo poner aqui uno q este dentro del JSON
    llista_trajecte = [[t_inicio.strftime("%H:%M:%S"), origen]]

    for i in range(len(stations)-1):
        actual = stations[i+1]
        llista_retallada = get_stop_ids_from_time(scheduler, linea, actual, sentido, t_inicio)
        closest_vector = get_closest_time_vector(llista_retallada, t_inicio)
        t_inicio = datetime.strptime(closest_vector["departure_time"], "%H:%M:%S").time()
        origen = closest_vector["stop_name"]
        llista_trajecte.append([t_inicio.strftime("%H:%M:%S"), origen])

    days = []
    time_list = []
    values_list = []

    for entry in travel["data"]:
        days.append(entry['day'])
        time_list.append(entry['time'])
        values_list.append(entry['connection'])

    # Crear el gráfico
    plt.figure(figsize=(14, 6))
    plt.plot(time_list, values_list, marker='o', linestyle='-')

    # Agregar el nombre de la estación en la hora correspondiente
    for time, station in llista_trajecte:
        plt.annotate(station, xy=(time, values_list[time_list.index(time)]), xytext=(5, 5), textcoords='offset points', ha='right')

    # Configurar etiquetas y título
    plt.xlabel('Tiempo y Estaciones')
    plt.ylabel('Valor')
    plt.title('Valores en el Tiempo y Estaciones')

    # Mostrar solo una de cada 10 etiquetas en el eje x
    x_ticks = range(0, len(time_list), 20)
    plt.xticks(x_ticks, [time_list[i] for i in x_ticks], rotation=45)

    # Mostrar el gráfico
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    __main__()
