import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# Load world shapefile
gdf_world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Load your data (replace 'temperature_data.csv' with your actual dataset)
# Assume the dataset contains columns: ['Country', 'Temperature_Change']
# Example: Country - USA, Canada, Mexico, etc., and Temperature_Change - the average temperature increase.
data = pd.read_csv('temperature_data.csv')

# Rename 'name' column to 'Country' for merging consistency
gdf_world.rename(columns={'name': 'Country'}, inplace=True)

# Merge GeoDataFrame with the temperature data
gdf = gdf_world.merge(data, on='Country', how='inner')

# Filter for countries in North and South America
gdf_americas = gdf[gdf['continent'].isin(['North America', 'South America'])]

# Plot the map
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
gdf_americas.plot(column='Temperature_Change', 
                  cmap='Reds', 
                  legend=True, 
                  legend_kwds={'label': "Average Temperature Increase (°C)"},
                  ax=ax)

# Add title
ax.set_title('Temperature Change in North and South America', fontsize=16)

# Remove axes for a cleaner map
ax.axis('off')

# Show plot
plt.show()