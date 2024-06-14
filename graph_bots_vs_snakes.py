import matplotlib.pyplot as plt
import pandas as pd

# Function to read data from a file and return it as a list of floats
def read_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        # Skip the header and convert lines to floats
        data = [float(line.strip()) for line in lines[1:]]
    return data

# Read data from files
data1 = read_data('./fov/snakes_fitness.csv')
data2 = read_data('./fov/bots_fitness.csv')

# Convert data to pandas Series
series1 = pd.Series(data1)
series2 = pd.Series(data2)

# Calculate rolling averages
window_size = 50
rolling_avg1 = series1.rolling(window=window_size).mean()
rolling_avg2 = series2.rolling(window=window_size).mean()

# Create a range for the x-axis
x1 = range(len(rolling_avg1))
x2 = range(len(rolling_avg2))

# Increase figure size
plt.figure(figsize=(14, 8))

# Plot the rolling averages
plt.plot(x1, rolling_avg1, label='Evolution Snakes Fitness (Rolling Avg)', linestyle='-')
plt.plot(x2, rolling_avg2, label='Bots Fitness (Rolling Avg)', linestyle='-')

# Add grid lines
plt.grid(True)

# Add labels and title
plt.xlabel('Round')
plt.ylabel('Fitness')
plt.title('Bot vs fov Snakes with limited view')
plt.legend()

# Show the plot
plt.show()
