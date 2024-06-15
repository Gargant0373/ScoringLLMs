import os
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get paths from environment variables
results_dir = os.getenv('RESULTS_DIR')

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

# Ensure only numeric columns are considered and exclude 'mxm_id'
numeric_data = data.select_dtypes(include=[float, int]).drop(columns=['mxm_id'], errors='ignore')

# Calculate the means of all numeric columns
means = numeric_data.mean().round(3)

# Calculate the standard deviations of all numeric columns
std_devs = numeric_data.std().round(3)

# Print out the means
print("\nMean values for each column:")
print(means.to_frame().transpose().to_string(index=False, header=True))

# Print out the standard deviations
print("\nStandard deviation for each column:")
print(std_devs.to_frame().transpose().to_string(index=False, header=True))
