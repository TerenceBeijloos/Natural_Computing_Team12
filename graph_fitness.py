import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
file_path = './GA.csv'
data = pd.read_csv(file_path)

# Print the data to verify
print(data)

# Plotting
plt.figure(figsize=(10, 6))

# Plot only the 'Fitness' column
if 'Fitness' in data.columns:
    plt.plot(data['Fitness'], label='Fitness')

# Adding labels and title
plt.xlabel('Index')
plt.ylabel('Fitness Value')
plt.title('Fitness Over Time')
plt.legend()

# Show the plot
plt.show()
