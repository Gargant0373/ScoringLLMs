import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get paths from environment variables
plot_path = os.getenv('PLOT_PATH')
results_dir = os.getenv('RESULTS_DIR')

# Create the directories if they don't exist
os.makedirs(plot_path, exist_ok=True)
os.makedirs(results_dir, exist_ok=True)

# List all CSV files in the results directory
csv_files = [f for f in os.listdir(results_dir) if f.endswith('.csv')]
print("Available CSV files:")
for idx, file in enumerate(csv_files):
    print(f"{idx + 1}. {file}")

# Ask the user to choose a file
file_index = int(input("Enter the number of the file you want to use: ")) - 1
file_path = os.path.join(results_dir, csv_files[file_index])

# Read the chosen CSV file
data = pd.read_csv(file_path)

# Create the heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(data.drop(columns=['mxm_id']).set_index(data['mxm_id']), annot=True, cmap='coolwarm', cbar=True)
plt.title('Values Heatmap')
plt.xlabel('Attributes')
plt.ylabel('MXM ID')

# Save the heatmap plot
heatmap_path = os.path.join(plot_path, 'values_heatmap.png')
plt.savefig(heatmap_path)

# Create histograms for each attribute
attributes = data.columns[1:]  # Exclude the 'mxm_id' column
for attribute in attributes:
    plt.figure(figsize=(8, 6))
    sns.histplot(data[attribute], kde=False, bins=5)
    plt.title(f'Histogram of {attribute}')
    plt.xlabel(attribute)
    plt.ylabel('Frequency')

    # Save the histogram plot
    histogram_path = os.path.join(plot_path, f'{attribute}_histogram.png')
    plt.savefig(histogram_path)
