import pandas as pd
import ssl
import numpy as np
import os
import plotly.express as px
from scipy.stats import linregress
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Disable SSL certificate verification (useful if there are SSL issues when fetching data from URLs).
ssl._create_default_https_context = ssl._create_unverified_context

def clean_dataset(df):
    """
    Cleans the dataset by removing duplicates, handling missing values, sorting the data,
    and dropping unnecessary columns.

    Parameters:
        df (DataFrame): The input dataset to be cleaned.

    Returns:
        DataFrame: The cleaned dataset.
    """
    # Remove duplicate rows from the dataset.
    df_cleaned = df.drop_duplicates()

    # Check if there are any missing values (NaN) in the dataset.
    if df_cleaned.isnull().any().any():
        # Fill NaN values in numeric columns with the mean of those columns.
        df_cleaned = df_cleaned.fillna(df_cleaned.mean(numeric_only=True))

    # If the dataset contains a "Year" column, sort the data by the "Year" column.
    if "Year" in df_cleaned.columns:
        df_cleaned = df_cleaned.sort_values(by="Year")

    # If the dataset contains an "ID" column, drop it as it is deemed unnecessary.
    if "ID" in df_cleaned.columns:
        df_cleaned = df_cleaned.drop(columns=["ID"])

    # Return the cleaned dataset.
    return df_cleaned

def fetch_data():
    """
    Fetches datasets for emissions and temperature from the specified URLs.

    Returns:
        tuple: A tuple containing two DataFrames:
            - emissions_data: The dataset for annual CO2 emissions by region.
            - temperature_data: The dataset for monthly average surface temperatures by year.
    """
    # Fetch the emissions dataset from the specified URL.
    # The URL points to a CSV file containing annual CO2 emissions data by region.
    emissions_data = pd.read_csv(
        "https://ourworldindata.org/grapher/annual-co-emissions-by-region.csv?v=1&csvType=full&useColumnShortNames=true",
        storage_options={'User-Agent': 'Our World In Data data fetch/1.0'}  # Specify a custom user-agent for the request.
    )

    # Fetch the temperature dataset from the specified URL.
    # The URL points to a CSV file containing monthly average surface temperature data by year.
    temperature_data = pd.read_csv(
        "https://ourworldindata.org/grapher/monthly-average-surface-temperatures-by-year.csv?v=1&csvType=full&useColumnShortNames=false",
        storage_options={'User-Agent': 'Our World In Data data fetch/1.0'}  # Specify a custom user-agent for the request.
    )

    # Return the two datasets as a tuple.
    return emissions_data, temperature_data


def transform_temperature_data(temperature_data):
    """
    Transforms the temperature dataset into a format suitable for analysis.

    Parameters:
        temperature_data (DataFrame): The original temperature dataset with columns for "Entity", "Code", "Year", and other data.

    Returns:
        DataFrame: A transformed temperature dataset where data is unpivoted and formatted for further analysis.
    """
    # Clean the dataset using a helper function (e.g., for missing values or invalid data).
    temperature_data = clean_dataset(temperature_data)

    # Ensure that column names representing years are converted to numeric types if possible.
    temperature_data.columns = [
        int(col) if col.isdigit() else col  # Convert column names to integers if they are numeric.
        for col in temperature_data.columns
    ]

    # Unpivot the dataset, transforming it from a wide format to a long format.
    # Columns "Entity", "Code", and "Year" are kept as identifiers (id_vars).
    # Other columns are melted into two: "Year_Column" (the original column name) and "Temperature" (the values).
    temperature_melted = temperature_data.melt(
        id_vars=["Entity", "Code", "Year"],  # Columns to keep as identifiers.
        var_name="Year_Column",  # Name for the new column representing the original column names.
        value_name="Temperature"  # Name for the new column representing the values.
    )

    # Convert the "Year_Column" to numeric values to ensure proper data type.
    temperature_melted["Year_Column"] = pd.to_numeric(temperature_melted["Year_Column"], errors="coerce")

    # Rename columns for clarity and consistency.
    temperature_melted.rename(columns={
        "Year_Column": "Year",  # Rename "Year_Column" to "Year".
        "Year": "Month"         # Rename the original "Year" column to "Month" (if this was intended).
    }, inplace=True)

    # Return the transformed dataset.
    return temperature_melted

def filter_data(temperature_data, emissions_data, regions):
    """
    Filters the temperature and emissions datasets for the specified regions and shared years.

    Parameters:
        temperature_data (DataFrame): The dataset containing temperature data, 
                                      with columns such as "Entity" and "Year".
        emissions_data (DataFrame): The dataset containing emissions data, 
                                    with columns such as "Entity" and "Year".
        regions (list): A list of region or country names to filter the data by.

    Returns:
        tuple: A tuple containing two filtered DataFrames:
            - temperature_filtered: The filtered temperature data for the specified regions and shared years.
            - emissions_filtered: The filtered emissions data for the specified regions and shared years.
    """
    # Filter the temperature dataset to include only rows where the "Entity" column matches the specified regions.
    temperature_filtered = temperature_data[temperature_data["Entity"].isin(regions)]

    # Filter the emissions dataset to include only rows where the "Entity" column matches the specified regions.
    emissions_filtered = emissions_data[emissions_data["Entity"].isin(regions)]

    # Find the years that are common between the filtered temperature and emissions datasets.
    common_years = set(temperature_filtered["Year"]).intersection(set(emissions_filtered["Year"]))

    # Further filter the datasets to include only rows with years in the common_years set.
    temperature_filtered = temperature_filtered[temperature_filtered["Year"].isin(common_years)]
    emissions_filtered = emissions_filtered[emissions_filtered["Year"].isin(common_years)]

    # Return the filtered datasets as a tuple.
    return temperature_filtered, emissions_filtered

def merge_datasets(temperature_data, emissions_data):
    """
    Merges the temperature and emissions datasets into a single dataset.

    Parameters:
        temperature_data (DataFrame): The dataset containing temperature data, 
                                      with columns such as "Entity" and "Year".
        emissions_data (DataFrame): The dataset containing emissions data, 
                                    with columns such as "Entity" and "Year".

    Returns:
        DataFrame: A combined dataset that includes data from both temperature_data 
                   and emissions_data, matched on "Entity" and "Year".
    """
    # Perform an inner merge on the "Entity" (country/region) and "Year" columns
    # to combine temperature and emissions data where both datasets have matching values.
    combined_data = pd.merge(
        temperature_data,  # First dataset: temperature data.
        emissions_data,    # Second dataset: emissions data.
        on=["Entity", "Year"],  # Columns to merge on: "Entity" and "Year".
        how="inner"  # Use an inner join to include only matching rows from both datasets.
    )
    
    # Return the merged dataset.
    return combined_data


def plot_emissions_by_country_large_graph(emissions_data_na, countries_na, region_na, 
                                          emissions_data_sa, countries_sa, region_sa, output_file):
    """
    Creates a large side-by-side graph for CO2 emissions by countries in two regions 
    and saves it as an image.

    Parameters:
        emissions_data_na (DataFrame): CO2 emissions data for the first region (e.g., North America).
        countries_na (list): List of country names for the first region.
        region_na (str): Name of the first region.
        emissions_data_sa (DataFrame): CO2 emissions data for the second region (e.g., South America).
        countries_sa (list): List of country names for the second region.
        region_sa (str): Name of the second region.
        output_file (str): File path to save the output image.
    """
    # Filter data for the specified countries in each region
    region_data_na = emissions_data_na[emissions_data_na["Entity"].isin(countries_na)]
    region_data_sa = emissions_data_sa[emissions_data_sa["Entity"].isin(countries_sa)]

    # Create subplots for side-by-side visualization
    fig = make_subplots(
        rows=1, cols=2, 
        subplot_titles=(f"CO2 Emissions in {region_na}", f"CO2 Emissions in {region_sa}")
    )

    # Add North America data to the first subplot
    for country in countries_na:
        country_data = region_data_na[region_data_na["Entity"] == country]
        fig.add_trace(
            go.Scatter(
                x=country_data["Year"], 
                y=country_data["emissions_total"], 
                mode='lines', 
                name=f"{country} ({region_na})"
            ),
            row=1, col=1
        )

    # Add South America data to the second subplot
    for country in countries_sa:
        country_data = region_data_sa[region_data_sa["Entity"] == country]
        fig.add_trace(
            go.Scatter(
                x=country_data["Year"], 
                y=country_data["emissions_total"], 
                mode='lines', 
                name=f"{country} ({region_sa})"
            ),
            row=1, col=2
        )

    # Customize the layout
    fig.update_layout(
        title_text="CO2 Emissions by Country: North America vs. South America",
        title_font_size=20,
        showlegend=True,
        legend_title_text="Countries",
        xaxis_title="Year",
        yaxis_title="CO2 Emissions (Million Tons)",
        height=600,  # Height of the graph in pixels
        width=1000   # Width of the graph in pixels
    )

    # Save the graph as an image
    fig.write_image(output_file)
    print(f"The graph has been successfully saved as '{output_file}'.")



def plot_temperature_by_region_large_graph(temp_data_na, countries_na, region_na, 
                                           temp_data_sa, countries_sa, region_sa, output_file):
    """
    Creates a large side-by-side graph comparing temperatures for two regions and saves it as an image file.

    Parameters:
        temp_data_na (DataFrame): Temperature data for North America.
        countries_na (list): List of countries in North America.
        region_na (str): Name of the North American region.
        temp_data_sa (DataFrame): Temperature data for South America.
        countries_sa (list): List of countries in South America.
        region_sa (str): Name of the South American region.
        output_file (str): File path to save the output image.
    """
    # Filter data for the specified countries
    region_data_na = temp_data_na[temp_data_na["Entity"].isin(countries_na)]
    region_data_sa = temp_data_sa[temp_data_sa["Entity"].isin(countries_sa)]

    # Create subplots
    fig = make_subplots(
        rows=1, cols=2, 
        subplot_titles=(f"Temperatures in {region_na}", f"Temperatures in {region_sa}")
    )

    # Add data for North America
    for country in countries_na:
        country_data = region_data_na[region_data_na["Entity"] == country]
        fig.add_trace(
            go.Scatter(
                x=country_data["Year"], 
                y=country_data["Temperature"], 
                mode='lines', 
                name=f"{country} ({region_na})"
            ),
            row=1, col=1
        )

    # Add data for South America
    for country in countries_sa:
        country_data = region_data_sa[region_data_sa["Entity"] == country]
        fig.add_trace(
            go.Scatter(
                x=country_data["Year"], 
                y=country_data["Temperature"], 
                mode='lines', 
                name=f"{country} ({region_sa})"
            ),
            row=1, col=2
        )

    # Customize layout
    fig.update_layout(
        title_text="Temperature Trends: North America vs. South America",
        title_font_size=20,
        showlegend=True,
        legend_title_text="Countries",
        xaxis=dict(title="Year"),
        yaxis=dict(title="Temperature (°C)"),
        height=600,  # Set the height of the graph
        width=1000   # Set the width of the graph
    )

    # Save the graph as an image
    fig.write_image(output_file)
    print(f"The graph has been successfully saved as '{output_file}'.")

def plot_temperature_vs_emissions(df_combined, output_file, width=1000, height=600, polynomial_degree=3):
    """
    Creates a scatter plot showing temperature as a function of total emissions, 
    including a polynomial regression line.

    Parameters:
        df_combined (DataFrame): A DataFrame containing columns "emissions_total", 
                                 "Temperature", "Region", and "Year".
        output_file (str): File path to save the image.
        width (int): Width of the saved image in pixels (default is 1920).
        height (int): Height of the saved image in pixels (default is 1080).
        polynomial_degree (int): Degree of the polynomial for regression (default is 3).
    """

    # Extract x (emissions) and y (temperature) data
    x = df_combined["emissions_total"].values
    y = df_combined["Temperature"].values

    # Sort x und y gemeinsam, damit die Trendlinie nachher "glatt" verläuft
    # (Sortierung basierend auf den x-Werten)
    sort_idx = np.argsort(x)
    x_sorted = x[sort_idx]
    y_sorted = y[sort_idx]

    # Compute the polynomial regression
    coeffs = np.polyfit(x_sorted, y_sorted, deg=polynomial_degree)
    # Berechne für die sortierten x-Werte die entsprechenden y-Werte der Regressionskurve
    trendline = np.polyval(coeffs, x_sorted)

    # Create scatter plot (Punktwolke)
    fig = px.scatter(
        df_combined,
        x="emissions_total",
        y="Temperature",
        color="Region",  # Group data points by region
        title="Temperature vs. CO2 Emissions (Polynom-Regressionsgrad = {})".format(polynomial_degree),
        labels={
            "emissions_total": "CO2 Emissions (Million Tons)",
            "Temperature": "Temperature (°C)"
        },
        hover_data=["Year"]  # Display additional information on hover
    )

    # Add the polynomial regression line
    fig.add_trace(
        go.Scatter(
            x=x_sorted,
            y=trendline,
            mode='lines',
            name='Polynomial Regression (Degree={})'.format(polynomial_degree),
            line=dict(color='red', width=2)
        )
    )

    # Save the graph as an image with specified dimensions
    fig.write_image(output_file, width=width, height=height)

def plot_temperature_with_trendlines(df_combined, p_values_df, output_file, width=1600, height=800):
    """
    Creates an interactive Plotly chart displaying temperature data with trendlines and p-values.

    Parameters:
        df_combined (DataFrame): A DataFrame containing columns "Region", "Year", and "Temperature".
        p_values_df (DataFrame): A DataFrame with p-values and regression details for each region.
        output_file (str): The file path to save the output image.
        width (int): The width of the saved image in pixels.
        height (int): The height of the saved image in pixels.
    """
    # Initialize a Plotly figure
    fig = go.Figure()

    # Iterate through each unique region to plot temperature data and trendlines
    for region in df_combined["Region"].unique():
        # Filter data for the current region
        region_data = df_combined[df_combined["Region"] == region]
        x = region_data["Year"]
        y = region_data["Temperature"]

        # Plot temperature data as a line
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            mode="lines",
            name=f"{region} Temperature",  # Region name in the legend
            line=dict(width=2),  # Line thickness
            hovertemplate="Year: %{x}<br>Temperature: %{y:.2f}°C<extra></extra>"  # Hover information
        ))

        # Fit a polynomial trendline (degree 4 for better fit)
        coeffs = np.polyfit(x, y, deg=4)  # Compute the coefficients of a 4th-degree polynomial
        trendline = np.polyval(coeffs, x)  # Evaluate the polynomial on x-values

        # Add the trendline to the chart
        fig.add_trace(go.Scatter(
            x=x,
            y=trendline,
            mode="lines",
            name=f"{region} Trendline",  # Trendline label in the legend
            line=dict(dash="dash"),  # Dashed line style for the trendline
            hovertemplate="Year: %{x}<br>Trendline: %{y:.2f}°C<extra></extra>"  # Hover info for the trendline
        ))

    # Customize the chart layout
    fig.update_layout(
        title="Temperature Changes in North and South America with Trendlines",  # Chart title
        xaxis_title="Year",  # Label for the x-axis
        yaxis_title="Temperature (°C)",  # Label for the y-axis
        legend_title="Regions",  # Legend title
        template="plotly_white",  # Use a white background template
        hovermode="x unified"  # Combine hover information for all traces
    )

    # Save the chart as an image with specified dimensions
    fig.write_image(output_file, width=width, height=height)  # Export the chart to the specified file

def calculate_p_values(df_combined):
    """
    Calculates linear regression and p-values for each region in the dataset.

    Parameters:
        df_combined (DataFrame): A DataFrame containing columns "Region", "Year", and "emissions_total".
        
    Returns:
        DataFrame: A new DataFrame with linear regression results, including slope, intercept, R-squared, and p-value for each region.
    """
    import pandas as pd
    from scipy.stats import linregress

    # Initialize a list to store the regression results for each region
    results = []

    # Iterate over each unique region in the DataFrame
    for region in df_combined["Region"].unique():
        # Filter the data for the current region
        region_data = df_combined[df_combined["Region"] == region]
        x = region_data["Year"].values  # Independent variable
        y = region_data["emissions_total"].values  # Dependent variable

        # Perform linear regression
        slope, intercept, r_value, p_value, std_err = linregress(x, y)

        # Append the regression results for the region to the results list
        results.append({
            "Region": region,
            "Slope": slope,  # The rate of change in emissions over time
            "Intercept": intercept,  # The estimated emissions at Year=0
            "R-squared": r_value**2,  # Coefficient of determination, indicates goodness of fit
            "P-value": p_value  # Statistical significance of the slope
        })

    # Convert the results list into a DataFrame for easier analysis and visualization
    return pd.DataFrame(results)


def main():
    # Fetch the emissions and temperature datasets from the source.
    # The function fetch_data() retrieves and returns these datasets as emissions_data and temperature_data.
    emissions_data, temperature_data = fetch_data()

    # Transform the temperature data into a format suitable for analysis.
    # The function transform_temperature_data() processes the raw temperature_data, 
    # such as reshaping or cleaning it, and returns the transformed dataset as temperature_melted.
    temperature_melted = transform_temperature_data(temperature_data)

    save_directory = os.path.join(os.path.dirname(__file__), "data")

    # Sicherstellen, dass das Speicherverzeichnis existiert
    os.makedirs(save_directory, exist_ok=True)

    # Define a list of countries that are part of the North American region.
    north_america_countries = [
        "Antigua and Barbuda", "Bahamas", "Belize", "Costa Rica",
        "Dominican Republic", "El Salvador", "Haiti", "Honduras", 
        "Jamaica", "Canada", "Cuba", "Mexico", "Nicaragua", 
        "Panama", "Trinidad and Tobago", "United States"
    ]

    # Define a list of countries that are part of the South American region.
    south_america_countries = [
        "Argentina", "Bolivia", "Brazil", "Chile", "Ecuador",
        "Guyana", "Colombia", "Paraguay", "Peru", "Suriname",
        "Uruguay", "Venezuela", "Guatemala"
    ]

    # Combine the lists for North America and South America into a single list of countries 
    # representing all of the Americas.
    all_americas = north_america_countries + south_america_countries

    # Group the melted temperature dataset (temperature_melted) by "Entity" (country/region) and "Year",
    # and calculate the average temperature for each combination of entity and year.
    yearly_summary_n = temperature_melted.groupby(["Entity", "Year"]).agg({
        "Temperature": "mean",  # Calculate the mean temperature for each group.
    }).reset_index()  # Reset the index to turn the grouped data into a standard dataframe.

    # Rename the columns for better clarity and formatting (though in this case, the column names are unchanged).
    yearly_summary_n.rename(columns={
        "Entity": "Entity",  # Rename "Entity" to "Entity" (redundant here but could be adjusted for consistency).
        "Year": "Year",      # Rename "Year" to "Year".
        "Temperature": "Temperature"  # Rename "Temperature" to "Temperature".
    }, inplace=True)

    # Filter the yearly summary dataset (yearly_summary_n) and the emissions dataset (emissions_data) 
    # to include only data for countries in North America (north_america_countries). 
    # This results in two filtered datasets: 
    # - yearly_summary_na_filtered: Filtered yearly summary data for North America.
    # - emissions_filtered_na: Filtered emissions data for North America.
    yearly_summary_na_filtered, emissions_filtered_na = filter_data(yearly_summary_n, emissions_data, north_america_countries)

    # Merge the filtered yearly summary for North America (yearly_summary_na_filtered) 
    # with the filtered emissions data for North America (emissions_filtered_na) 
    # into a single dataset named "combined_filtered_data_na".
    combined_filtered_data_na = merge_datasets(yearly_summary_na_filtered, emissions_filtered_na)

    # Group the filtered dataset for North America (combined_filtered_data_na) by "Year" 
    # and calculate the yearly values for each group.
    yearly_summarynorden = combined_filtered_data_na.groupby("Year").agg({
        "Temperature": "mean",  # Calculate the average temperature for all months within each year.
        "emissions_total": "sum"  # Calculate the total emissions for all months within each year.
    }).reset_index()  # Reset the index to convert the grouped data back into a standard dataframe.

    # Filter and merge datasets for North America
    yearly_summary_sa_filtered, emissions_filtered_na = filter_data(yearly_summary_n, emissions_data, south_america_countries)

    # Merge the filtered yearly summary for South America (yearly_summary_sa_filtered) 
    # with the filtered emissions data for North America (emissions_filtered_na) into a new dataset called "sueden".
    sueden = merge_datasets(yearly_summary_sa_filtered, emissions_filtered_na)

    # Grouping data by 'Year' and calculating annual statistics
    yearly_summarysouth = sueden.groupby("Year").agg({
        "Temperature": "mean",  # Calculate the average temperature across all months for each year
        "emissions_total": "sum"  # Sum the total emissions across all months for each year
    }).reset_index()

    # Add a new column "Region" to the yearly summary for North America and set its value to "Nordamerika".
    yearly_summarynorden["Region"] = "Nordamerika"

    # Add a new column "Region" to the yearly summary for South America and set its value to "Südamerika".
    yearly_summarysouth["Region"] = "Südamerika"

    # Combine the dataframes for North America and South America into one, 
    # ignoring the original index values to create a new continuous index.
    df_combined = pd.concat([yearly_summarynorden, yearly_summarysouth], ignore_index=True)

    # Generate plots and save them in the relative directory
    plot_temperature_by_region_large_graph(
        combined_filtered_data_na, north_america_countries, "Nordamerika",
        sueden, south_america_countries, "Südamerika",
        os.path.join(save_directory, "temperature_large_graph.pdf")
    )

    plot_emissions_by_country_large_graph(
        combined_filtered_data_na, north_america_countries, "Nordamerika",
        sueden, south_america_countries, "Südamerika",
        os.path.join(save_directory, "co2_emissions_large_graph.pdf")
    )

    plot_temperature_vs_emissions(
        df_combined, os.path.join(save_directory, "temperature_vs_emissions.pdf")
    ) 

    # Calculate p-values for statistical significance testing
    p_values_df = calculate_p_values(df_combined)

    # Display the resulting p-values and regression results
    print("\nP-values and regression results:")
    print(p_values_df)

    plot_temperature_with_trendlines(
        df_combined, p_values_df,
        os.path.join(save_directory, "temperature_trendlines.pdf")
    )

    # Save datasets in the relative directory
    df_combined.to_csv(os.path.join(save_directory, 'df_combined.csv'), index=False)
    yearly_summarysouth.to_csv(os.path.join(save_directory, 'yearly_summarysouth.csv'), index=False)
    yearly_summarynorden.to_csv(os.path.join(save_directory, 'yearly_summarynorden.csv'), index=False)

if __name__ == "__main__":
    main()