import pandas as pd
import ssl
import numpy as np
from scipy.stats import linregress
import geopandas as gpd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Disable SSL certificate verification
ssl._create_default_https_context = ssl._create_unverified_context

def clean_dataset(df):
    """Cleans the dataset: removes duplicates, handles missing values, sorts, and drops unnecessary columns."""
    df_cleaned = df.drop_duplicates()

    # Handle missing values (NaN)
    if df_cleaned.isnull().any().any():
        # Fill NaN values with the mean of numeric columns
        df_cleaned = df_cleaned.fillna(df_cleaned.mean(numeric_only=True))

    # Sort data by a specific column (e.g., Year)
    if "Year" in df_cleaned.columns:
        df_cleaned = df_cleaned.sort_values(by="Year")

    # Drop irrelevant columns (e.g., ID)
    if "ID" in df_cleaned.columns:
        df_cleaned = df_cleaned.drop(columns=["ID"])

    return df_cleaned

def fetch_data():
    """Fetches datasets from the specified URLs."""
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
    """Transforms the temperature dataset into an analyzable format."""
    temperature_data = clean_dataset(temperature_data)

    # Ensure column names for years are numeric
    temperature_data.columns = [
        int(col) if col.isdigit() else col
        for col in temperature_data.columns
    ]

    # Unpivot temperature data
    temperature_melted = temperature_data.melt(
        id_vars=["Entity", "Code", "Year"],
        var_name="Year_Column",
        value_name="Temperature"
    )

    # Convert 'Year_Column' to numeric values
    temperature_melted["Year_Column"] = pd.to_numeric(temperature_melted["Year_Column"], errors="coerce")

    # Rename columns
    temperature_melted.rename(columns={"Year_Column": "Year", "Year": "Month"}, inplace=True)

    return temperature_melted

def filter_data(temperature_data, emissions_data, regions):
    """Filters the temperature and emissions data for the specified regions and shared years."""
    print(f"[DEBUG] Filtering data for regions: {regions}...")
    temperature_filtered = temperature_data[temperature_data["Entity"].isin(regions)]
    emissions_filtered = emissions_data[emissions_data["Entity"].isin(regions)]

    # Find common years
    common_years = set(temperature_filtered["Year"]).intersection(set(emissions_filtered["Year"]))

    temperature_filtered = temperature_filtered[temperature_filtered["Year"].isin(common_years)]
    emissions_filtered = emissions_filtered[emissions_filtered["Year"].isin(common_years)]

    print("[DEBUG] Data filtered. Saving intermediate results...")
    temperature_filtered.to_csv("filtered_temperature_data.csv", index=False)
    emissions_filtered.to_csv("filtered_emissions_data.csv", index=False)
    print("[DEBUG] Filtered temperature data saved to 'filtered_temperature_data.csv'.")
    print("[DEBUG] Filtered emissions data saved to 'filtered_emissions_data.csv'.")

    return temperature_filtered, emissions_filtered

def merge_datasets(temperature_data, emissions_data):
    """Merges the temperature and emissions datasets into a single dataset."""
    combined_data = pd.merge(
        temperature_data,
        emissions_data,
        on=["Entity", "Code", "Year"],
        how="inner"
    )
    return combined_data

def plot_temperature_with_trendlines(df_combined, p_values_df):
    """Erstellt eine Plotly-Grafik, die Temperaturdaten mit Trendlinien und P-Werten anzeigt."""
    fig = go.Figure()

    # Durch Regionen iterieren und Temperaturdaten mit Trendlinien hinzufügen
    for region in df_combined["Region"].unique():
        region_data = df_combined[df_combined["Region"] == region]
        x = region_data["Year"]
        y = region_data["Temperature"]

        # Plot Temperaturdaten
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            mode="lines",
            name=f"{region} Temperatur",
            line=dict(width=2),
            hovertemplate="Jahr: %{x}<br>Temperatur: %{y:.2f}°C<extra></extra>"
        ))

        # Lineare Regression berechnen
        coeffs = np.polyfit(x, y, deg=4)
        trendline = np.polyval(coeffs, x)

        # Trendlinie hinzufügen
        fig.add_trace(go.Scatter(
            x=x,
            y=trendline,
            mode="lines",
            name=f"{region} Trendlinie",
            line=dict(dash="dash"),
            hovertemplate="Jahr: %{x}<br>Trendlinie: %{y:.2f}°C<extra></extra>"
        ))

    # Layout anpassen
    fig.update_layout(
        title="Temperaturänderungen in Nord- und Südamerika mit Trendlinien",
        xaxis_title="Jahr",
        yaxis_title="Temperatur (°C)",
        legend_title="Regionen",
        template="plotly_white"
    )

    # Grafik anzeigen
    fig.show()


def plot_temperature_vs_emissions(df_combined):
    """
    Erstellt ein Streudiagramm, das die Temperatur in Abhängigkeit der Emissionen zeigt,
    inklusive einer Regressionslinie.
    """
    # Regressionslinie berechnen
    x = df_combined["emissions_total"]
    y = df_combined["Temperature"]

    coeffs = np.polyfit(x, y, deg=1)  # lineare Regression
    trendline = np.polyval(coeffs, x)

    # Streudiagramm erstellen
    fig = px.scatter(
        df_combined,
        x="emissions_total",
        y="Temperature",
        color="Region",
        title="Temperatur in Abhängigkeit von CO2-Emissionen",
        labels={"emissions_total": "CO2-Emissionen (Millionen Tonnen)", "Temperature": "Temperatur (°C)"},
        hover_data=["Year"]
    )

    # Grafik anzeigen
    fig.show()

def calculate_p_values(df_combined):
    """Berechnet die lineare Regression und die p-Werte für jede Region."""
    results = []
    
    for region in df_combined["Region"].unique():
        region_data = df_combined[df_combined["Region"] == region]
        x = region_data["Year"].values
        y = region_data["emissions_total"].values

        # Lineare Regression
        slope, intercept, r_value, p_value, std_err = linregress(x, y)

        # Ergebnisse speichern
        results.append({
            "Region": region,
            "Slope": slope,
            "Intercept": intercept,
            "R-squared": r_value**2,
            "P-value": p_value
        })

    return pd.DataFrame(results)



def plot_emissions_by_country(emissions_data, region_countries, region_name):
    """Erstellt ein interaktives Liniendiagramm der CO2-Emissionen für alle Länder einer Region."""
    # Daten filtern
    region_data = emissions_data[emissions_data["Entity"].isin(region_countries)]

    # Interaktives Plotly-Diagramm erstellen
    fig = px.line(
        region_data,
        x="Year",
        y="emissions_total",
        color="Entity",
        title=f"CO2-Emissionen in {region_name} nach Ländern",
        labels={"emissions_total": "CO2-Emissionen (Millionen Tonnen)", "Year": "Jahr", "Entity": "Land"}
    )

    # Layout anpassen
    fig.update_layout(
        legend_title_text="Länder",
        title_font_size=16,
        xaxis_title_font_size=12,
        yaxis_title_font_size=12
    )

    # Grafik anzeigen
    fig.show()


def main():
    """Main function to execute the data pipeline."""
    # Fetch data
    emissions_data, temperature_data = fetch_data()

    # Transform temperature data
    temperature_melted = transform_temperature_data(temperature_data)

    # Define regions
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

   # -------------------
    # NORDAMERIKA
    # -------------------
    temperature_filtered_na, emissions_filtered_na = filter_data(temperature_melted, emissions_data, north_america_countries)
    combined_filtered_data_na = merge_datasets(temperature_filtered_na, emissions_filtered_na)

    combined_filtered_data_na.to_csv("north_america_datal.csv", index=False)


    # Gruppieren nach Year und Berechnung des Durchschnitts der Temperaturen und Summe der Emissionen
    combined_filtered_data_na = combined_filtered_data_na.groupby("Month").agg({
        "Temperature": "mean",  # Durchschnittstemperatur
        "emissions_total": "sum"  # Gesamtemissionen
    }).reset_index()

    combined_filtered_data_na.to_csv("north_america_data.csv", index=False)
    print("Die gefilterten Daten für Nordamerika wurden als 'north_america_data.csv' gespeichert.")


    # -------------------
    # SÜDAMERIKA
    # -------------------
    temperature_filtered_sa, emissions_filtered_sa = filter_data(temperature_melted, emissions_data, south_america_countries)
    combined_filtered_data_sa = merge_datasets(temperature_filtered_sa, emissions_filtered_sa)

    combined_filtered_data_sa.to_csv(".csv", index=False)

    # Gruppieren nach Year und Berechnung des Durchschnitts der Temperaturen und Summe der Emissionen
    combined_filtered_data_sa = combined_filtered_data_sa.groupby("Year").agg({
        "Temperature": "mean",  # Durchschnittstemperatur
        "emissions_total": "sum"  # Gesamtemissionen
    }).reset_index()

    combined_filtered_data_sa.to_csv("south_america_data.csv", index=False)
    print("Die gefilterten Daten für Südamerika wurden als 'south_america_data.csv' gespeichert.")

    # -------------------
    # ALLE AMERIKAS
    # -------------------
    temperature_filtered, emissions_filtered = filter_data(temperature_melted, emissions_data, all_americas)
    combined_filtered_data = merge_datasets(temperature_filtered, emissions_filtered)

    combined_filtered_data.to_csv("datal.csv", index=False)

    # Gruppieren nach Year und Berechnung des Durchschnitts der Temperaturen und Summe der Emissionen
    combined_filtered_data = combined_filtered_data.groupby("Year").agg({
        "Temperature": "mean",  # Durchschnittstemperatur
        "emissions_total": "sum"  # Gesamtemissionen
    }).reset_index()

    combined_filtered_data.to_csv("filtered_combined_temperature_emissions.csv", index=False)
    print("Data for all Americas has been successfully saved in 'filtered_combined_temperature_emissions.csv'.")

    # Daten laden
    df_na = pd.read_csv("north_america_data.csv")
    df_sa = pd.read_csv("south_america_data.csv")

    # Region hinzufügen, um die Daten zu unterscheiden
    df_na["Region"] = "Nordamerika"
    df_sa["Region"] = "Südamerika"

    # Daten kombinieren
    df_combined = pd.concat([df_na, df_sa], ignore_index=True)

    # P-Wert-Berechnung
    p_values_df = calculate_p_values(df_combined)
    print("\nP-Werte und Regressionsergebnisse:")
    print(p_values_df)

    # Grafik erstellen
    fig = px.line(
        df_combined,
        x="Year",
        y="emissions_total",
        color="Region",
        title="CO2-Emissionen in Nord- und Südamerika über die Jahre",
        labels={"emissions_total": "CO2-Emissionen", "Year": "Jahr"}
    )

    # Trendlinie manuell berechnen und hinzufügen
    for region in df_combined["Region"].unique():
        region_data = df_combined[df_combined["Region"] == region]
        x = region_data["Year"]
        y = region_data["emissions_total"]

        # Lineare Regression berechnen
        coeffs = np.polyfit(x, y, deg=4)
        trendline = np.polyval(coeffs, x)

        # Trendlinie zur Grafik hinzufügen
        fig.add_scatter(
            x=x,
            y=trendline,
            mode="lines",
            name=f"Trendline ({region})",
            line=dict(dash="dash")  # Linie gestrichelt darstellen
        )

    # Grafik anzeigen
    fig.show()

     # Daten filtern für Nord- und Südamerika
    north_america_emissions = emissions_data[emissions_data["Entity"].isin(north_america_countries)]
    south_america_emissions = emissions_data[emissions_data["Entity"].isin(south_america_countries)]

     # Diagramme erstellen
    print("Erstelle Grafik für Nordamerika...")
    plot_emissions_by_country(north_america_emissions, north_america_countries, "Nordamerika")

    print("Erstelle Grafik für Südamerika...")
    plot_emissions_by_country(south_america_emissions, south_america_countries, "Südamerika")

    # Aufruf der Funktion
    plot_temperature_with_trendlines(df_combined, p_values_df)

    plot_temperature_vs_emissions(df_combined)

    # Emissions- und Temperaturdaten laden (aus vorhandenen CSV-Dateien)
    emissions_data = pd.read_csv("filtered_combined_temperature_emissions.csv")
    temperature_data = pd.read_csv("filtered_combined_temperature_emissions.csv")

if __name__ == "__main__":
    main()
