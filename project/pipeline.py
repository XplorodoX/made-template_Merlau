import pandas as pd
import ssl

# SSL-Zertifikatsüberprüfung deaktivieren
ssl._create_default_https_context = ssl._create_unverified_context

def clean_dataset(df):
    """Bereinigt den Datensatz: Duplikate entfernen, fehlende Werte behandeln, sortieren, unnötige Spalten entfernen."""
    df_cleaned = df.drop_duplicates()

    # Handle missing values (NaN)
    if df_cleaned.isnull().any().any():
        # Drop rows with NaN values
        df_cleaned = df_cleaned.fillna(df_cleaned.mean(numeric_only=True))

    # Sort data by a specific column (e.g., Year)
    if "Year" in df_cleaned.columns:
        df_cleaned = df_cleaned.sort_values(by="Year")

    # Drop irrelevant columns (e.g., ID)
    if "ID" in df_cleaned.columns:
        df_cleaned = df_cleaned.drop(columns=["ID"])

    return df_cleaned

def fetch_data():
    """Lädt die Datensätze von den entsprechenden URLs herunter."""
    emissions_data = pd.read_csv(
        "https://ourworldindata.org/grapher/annual-co-emissions-by-region.csv?v=1&csvType=full&useColumnShortNames=true",
        storage_options={'User-Agent': 'Our World In Data data fetch/1.0'}
    )

    temperature_data = pd.read_csv(
        "https://ourworldindata.org/grapher/monthly-average-surface-temperatures-by-year.csv?v=1&csvType=full&useColumnShortNames=false",
        storage_options={'User-Agent': 'Our World In Data data fetch/1.0'}
    )

    return emissions_data, temperature_data

def transform_temperature_data(temperature_data):
    """Transformiert die Temperaturdaten in ein analysierbares Format."""
    temperature_data = clean_dataset(temperature_data)

    # Sicherstellen, dass Spaltennamen für Jahreszahlen numerisch sind
    temperature_data.columns = [
        int(col) if col.isdigit() else col
        for col in temperature_data.columns
    ]

    # Temperaturdaten umformen (unpivotieren)
    temperature_melted = temperature_data.melt(
        id_vars=["Entity", "Code", "Year"],
        var_name="Year_Column",
        value_name="Temperature"
    )

    # 'Year_Column' zu numerischen Werten umwandeln
    temperature_melted["Year_Column"] = pd.to_numeric(temperature_melted["Year_Column"], errors="coerce")

    # Spalten umbenennen
    temperature_melted.rename(columns={"Year_Column": "Year", "Year": "Month"}, inplace=True)

    return temperature_melted

def filter_data(temperature_data, emissions_data, regions):
    """Filtert die Temperatur- und Emissionsdaten für die angegebene Region und gemeinsame Jahre."""
    # Filter Daten für die Regionen
    temperature_filtered = temperature_data[temperature_data["Entity"].isin(regions)]
    emissions_filtered = emissions_data[emissions_data["Entity"].isin(regions)]

    # Gemeinsame Jahre finden
    common_years = set(temperature_filtered["Year"]).intersection(set(emissions_filtered["Year"]))

    # Filter auf gemeinsame Jahre anwenden
    temperature_filtered = temperature_filtered[temperature_filtered["Year"].isin(common_years)]
    emissions_filtered = emissions_filtered[emissions_filtered["Year"].isin(common_years)]

    return temperature_filtered, emissions_filtered

def merge_datasets(temperature_data, emissions_data):
    """Verbindet die Temperatur- und Emissionsdaten in einem Datensatz."""
    combined_data = pd.merge(
        temperature_data,
        emissions_data,
        on=["Entity", "Code", "Year"],
        how="inner"
    )
    return combined_data

def main():
    """Hauptfunktion zum Ausführen der Datenpipeline."""
    # Daten abrufen
    emissions_data, temperature_data = fetch_data()

    # Temperaturdaten transformieren
    temperature_melted = transform_temperature_data(temperature_data)

    # Regionen definieren
    north_america_countries = [
        "Antigua and Barbuda", "Bahamas", "Belize", "Costa Rica",
        "Dominican Republic", "El Salvador", "Haiti", "Honduras", 
        "Jamaica", "Canada", "Cuba", "Mexico", "Nicaragua", 
        "Panama", "Trinidad and Tobago", "United States"
    ]

    south_america_countries = [
        "Argentina", "Bolivia", "Brazil", "Chile", "Ecuador",
        "Guyana", "Colombia", "Paraguay", "Peru", "Suriname",
        "Uruguay", "Venezuela", "Guatemala"
    ]

    all_americas = north_america_countries + south_america_countries

    # Daten filtern
    temperature_filtered, emissions_filtered = filter_data(temperature_melted, emissions_data, all_americas)

    # Datensätze verbinden
    combined_filtered_data = merge_datasets(temperature_filtered, emissions_filtered)

    # Ergebnis speichern
    combined_filtered_data.to_csv('filtered_combined_temperature_emissions.csv', index=False)
    print("Daten wurden erfolgreich gespeichert.")

if __name__ == "__main__":
    main()