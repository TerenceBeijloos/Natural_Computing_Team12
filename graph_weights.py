import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import os

# Function to generate and save plot for a CSV file
def generate_and_save_plot(file_path, save_dir):
    data = pd.read_csv(file_path)
    
    # Smoothing the data with a rolling average
    rolling_window = 20
    data_smoothed = data.rolling(window=rolling_window, min_periods=1).mean()
    
    # Creating a figure and axis
    fig, ax1 = plt.subplots(figsize=(14, 8))
    
    # Plot fitness on the secondary y-axis (background)
    ax2 = ax1.twinx()
    ax2.fill_between(data_smoothed.index, data_smoothed['Fitness'], color='red', alpha=0.2, label='Fitness')
    ax2.set_ylabel('Fitness', fontsize=12)
    
    # Distinct colors for each line
    colors = ['blue', 'orange', 'green', 'red', 'purple']
    
    # Plot all columns except "Fitness" on the primary y-axis
    for i, column in enumerate(data.columns):
        if column != 'Fitness':
            ax1.plot(data_smoothed[column], label=column, linewidth=1.5, color=colors[i % len(colors)], alpha=0.7)
    
    # Set labels and title for the primary y-axis
    ax1.set_xlabel('Round', fontsize=12)
    ax1.set_ylabel('Weight', fontsize=12)
    ax1.set_title(f'GA two food run 3 - {os.path.basename(file_path)}', fontsize=14)
    
    # Adding grid
    ax1.grid(True)
    
    # Adding legends for both axes
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    lines = lines_1 + lines_2
    labels = labels_1 + labels_2
    
    # Placing the legend outside the plot area
    ax1.legend(lines, labels, loc='center left', bbox_to_anchor=(1.1, 0.5), fontsize=10)
    
    # Adjust layout to make room for the legend
    plt.tight_layout(rect=[0, 0, 0.8, 1])
    
    # Save the plot
    plot_filename = os.path.join(save_dir, f'{os.path.splitext(os.path.basename(file_path))[0]}.png')
    plt.savefig(plot_filename)
    plt.close(fig)

# Path to the directory containing the CSV files
files_path = './limited_snakes/weights/*.csv'
files = glob.glob(files_path)

# Directory to save the plots
save_dir = './limited_snakes_plots'
os.makedirs(save_dir, exist_ok=True)

# Generate and save plot for each file
for file in files:
    generate_and_save_plot(file, save_dir)

print(f'Plots saved in {save_dir}')
