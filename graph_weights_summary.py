import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob

# Function to extract the last weights including fitness from a CSV file
def extract_last_weights(file_path):
    data = pd.read_csv(file_path)
    last_row = data.iloc[-1]
    last_weights = last_row.drop(labels='Fitness').tolist() + [last_row['Fitness']]
    return last_weights

# Path to the directory containing the CSV files
files_path = 'limited_snakes/weights/*.csv'
files = glob.glob(files_path)

# Colors for plotting
colors = plt.cm.rainbow(np.linspace(0, 1, len(files)))

# Plotting the weights
plt.figure(figsize=(10, 6))

for i, file in enumerate(files):
    last_weights = extract_last_weights(file)
    plt.plot(['Nearest food', 'General food', 'Nearest snake', 'General snake', 'Walls', 'Fitness'], 
             last_weights, marker='o', color=colors[i], label=f'Run {i+1}')

# Setting the labels and title
plt.xlabel('Weight')
plt.ylabel('Value')
plt.title('Last values from the limited snakes experiment')
plt.legend()
plt.grid(True)

# Show the plot
plt.show()
