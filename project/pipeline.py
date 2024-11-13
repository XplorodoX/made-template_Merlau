import pandas as pd
import requests
import sqlite3

#Warning, er gibt einen Fehler aus. 
# Fetch the data
df = pd.read_csv("https://ourworldindata.org/grapher/annual-co-emissions-by-region.csv?v=1&csvType=full&useColumnShortNames=false")

# Fetch the metadata
metadata = requests.get("https://ourworldindata.org/grapher/annual-co-emissions-by-region.metadata.json?v=1&csvType=full&useColumnShortNames=false").json()

# Filter rows with missing values
df_cleaned = df.dropna()

# Verbindung zur SQLite-Datenbank herstellen (oder eine neue erstellen)
conn = sqlite3.connect('data/cleaned_data.db')

# Das bereinigte DataFrame in die SQLite-Datenbank schreiben
df_cleaned.to_sql('cleaned_data', conn, if_exists='replace', index=False)

# Verbindung schließen
conn.close()