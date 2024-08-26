import geopandas as gpd

# Load the shapefile
shapefile_path = '/workspaces/IPL_LOYALTY_INDEX/india_states.shp'
india_map = gpd.read_file(shapefile_path)

# Print the columns to check
print(india_map.columns)
