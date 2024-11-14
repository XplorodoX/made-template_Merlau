import requests
import zipfile
import io
import pandas as pd

# URL der ZIP-Datei
url = 'https://datacatalogfiles.worldbank.org/ddh-published/0037712/DR0045575/WDI_CSV_2024_10_24.zip?versionId=2024-10-28T13:09:29.1647687Z'

# Herunterladen der ZIP-Datei
response = requests.get(url)
if response.status_code == 200:
    # Entpacken der ZIP-Datei
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        # Auflisten der enthaltenen Dateien
        file_list = z.namelist()
        print("Enthaltene Dateien:", file_list)
        
        # Laden der CSV-Dateien in Pandas DataFrames
        dataframes = {}
        for file_name in file_list:
            if file_name.endswith('.csv'):
                with z.open(file_name) as f:
                    df = pd.read_csv(f)
                    dataframes[file_name] = df
                    print(f"Datei '{file_name}' erfolgreich geladen.")
else:
    print(f"Fehler beim Herunterladen der Datei. Statuscode: {response.status_code}")

# Daten abrufen
df = pd.read_csv("https://ourworldindata.org/grapher/annual-co-emissions-by-region.csv?v=1&csvType=full&useColumnShortNames=false")

# Metadaten abrufen
metadata = requests.get("https://ourworldindata.org/grapher/annual-co-emissions-by-region.metadata.json?v=1&csvType=full&useColumnShortNames=false").json()

# Fehlende Werte entfernen
df_cleaned = df.dropna()

# Spaltentypen prüfen und ggf. konvertieren
print("Spaltentypen vor Konvertierung:")
print(df_cleaned.dtypes)

# Beispiel: Konvertierung der "Jahr"-Spalte in Ganzzahl, falls diese nicht bereits Integer ist
if 'Jahr' in df_cleaned.columns and df_cleaned['Jahr'].dtype != 'int64':
    df_cleaned['Jahr'] = pd.to_numeric(df_cleaned['Jahr'], errors='coerce').fillna(0).astype(int)

# Sicherstellen, dass der Ordner für die Datenbank existiert
db_path = 'project/data/cleaned_data.db'
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect(db_path)

# Bereinigtes DataFrame in die SQLite-Datenbank schreiben
df_cleaned.to_sql('cleaned_data', conn, if_exists='replace', index=False)

# Gespeicherte Daten abfragen und Datentypen prüfen
df_from_db = pd.read_sql('SELECT * FROM cleaned_data LIMIT 5', conn)
print("Spaltentypen nach Laden in die Datenbank:")
print(df_from_db.dtypes)

# Verbindung schließen
conn.close()


