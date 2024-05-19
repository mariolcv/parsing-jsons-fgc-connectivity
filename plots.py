import matplotlib.pyplot as plt
import main

def plot_signal_time_station(data):

    # Separate the data into x and t components
    connection = [item['connection'] for item in data]
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
data = main.loaders()
#print(data)
plot_signal_time_station(data[1]['data'])