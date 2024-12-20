import sqlite3
import requests
import zipfile
import io
import pandas as pd
import os

# URL of the ZIP file
url = 'https://datacatalogfiles.worldbank.org/ddh-published/0037712/DR0045575/WDI_CSV_2024_10_24.zip?versionId=2024-10-28T13:09:29.1647687Z'

# Download the ZIP file
response = requests.get(url)
if response.status_code == 200:
    # Extract the ZIP file
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        # Load the relevant CSV files into Pandas DataFrames
        with z.open('WDICSV.csv') as f:
            df = pd.read_csv(f)
        with z.open('WDICountry.csv') as f:
            supdata = pd.read_csv(f)
else:
    print(f"Error downloading the file. Status code: {response.status_code}")

# Step 1: Identify aggregated entries
aggregated_country_codes = supdata[supdata['Currency Unit'].isna()]['Country Code'].unique()

# Step 2: Remove aggregated data from df
filtered_data = df[~df['Country Code'].isin(aggregated_country_codes)]

# Reset the index
filtered_data.reset_index(drop=True, inplace=True)

# **Modify the database path to point to the parent directory**
# Get the parent directory of the current script
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Define the path to the SQLite database in the parent directory
db_path = os.path.join(parent_dir, 'data', 'cleaned_data.db')

# Ensure the 'data' directory exists in the parent directory
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Establish a connection to the SQLite database (or create a new one)
conn = sqlite3.connect(db_path)

# Write the cleaned DataFrame to the SQLite database
filtered_data.to_sql('cleaned_data', conn, if_exists='replace', index=False)

# Close the connection
conn.close()
