from datetime import datetime, date, timedelta
import matplotlib.pyplot as plt

def add_second_to_time(t):
    # Combine date and time to create a datetime object
    datetime_obj = datetime.combine(date.today(), t)    
    # Add one second
    new_datetime_obj = datetime_obj + timedelta(seconds=1)
    # Extract the time part
    new_time = new_datetime_obj.time()
    
    return new_time

def faltenMatrix(matrix, stations, o_time):
    time = o_time
    signal_time_station = []
    for list, stat in zip(matrix, stations):
        for l in list:
            signal_time_station.append({'signal': l,'time': time.strftime('%H:%M:%S') , 'station': stat})
            time = add_second_to_time(time)

    return signal_time_station


def plot_signal_time_station(signal_time_station):
    times = [entry['time'] for entry in signal_time_station]
    signals = [int(entry['signal']) for entry in signal_time_station]
    stations = [entry['station'] for entry in signal_time_station]

    plt.figure(figsize=(10, 6))
    plt.plot(times, signals, marker='o', linestyle='-')

    previous_station = None
    for i, (time, station) in enumerate(zip(times, stations)):
        if station != previous_station:
            plt.annotate(station, (time, signals[i]), textcoords="offset points", xytext=(0,10), ha='center')
            previous_station = station
            # Add the end of the station with a train stop
            if i + 1 < len(times) and times[i + 1] != times[i] and i + 1 < len(stations) and stations[i + 1] == station:
                plt.annotate(station, (times[i + 1], signals[i + 1]), textcoords="offset points", xytext=(0,10), ha='center')

    plt.xlabel('Time')
    plt.ylabel('Signal Value')
    plt.title('Signal Value over Time')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    
    
# Example usage
#data = main.loaders()
#print(data)
#plot_signal_time_station(data[1]['data'])