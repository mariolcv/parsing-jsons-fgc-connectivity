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
        
def plot_signal_time_station(data):

    # Separate the data into x and t components
    connection = [item['signal'] for item in data]
    time = [item['time'] for item in data]
    
    # Create a plot
    plt.figure(figsize=(10, 6))
    plt.plot(time, connection, marker='o', linestyle='-', color='b')
    
    # Add titles and labels
    plt.title('Signal though time')
    plt.xlabel('temps')
    plt.ylabel('Signal')
    
    # Display the plot
    # Hide the y-axis numbers
    plt.xticks([data[0]['time'], data[int(len(data)/4)]['time'], data[int(len(data)/2)]['time'], data[int(3*len(data)/4)]['time'], data[-1]['time']])
    plt.grid(True)
    plt.show()
    
    
# Example usage
#data = main.loaders()
#print(data)
#plot_signal_time_station(data[1]['data'])