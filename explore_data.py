import pandas as pd

# Load the CSV
data = pd.read_csv('compact.csv')

# Print column names
print("Available columns:")
print(data.columns.tolist())