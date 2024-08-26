import os
import shutil
import fiona
import pyproj
import pandas as pd
from pyproj import CRS
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.ops import transform
from shapely.geometry import shape, LineString
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import split

from ta_to_climate_zone import ta_to_climate_zone
from process_river import load_and_process_river


#### Constants

RANGITIKEI_SPLIT_LINE = LineString([(lon, -39.833333333) for lon in (175.41445, 175.80)])
OTEKAIEKE_END_POINTS = [(170.333, -44.904), (170.5846, -44.815)] # Force the river to cross the TA boundary
OTEKAIEKE = load_and_process_river('Otekaieke River', OTEKAIEKE_END_POINTS)  # Get the river geometry, removing braiding and extending to just past the TA boundary
DIRECTORY_PATH = "./statsnz-territorial-authority-2023-clipped-generalised-SHP"
SHAPEFILE_NAME = "territorial-authority-2023-clipped-generalised.shp"
SHAPEFILE_PATH = f"{DIRECTORY_PATH}/{SHAPEFILE_NAME}"
OUTPUT_PATH = "./output"


#### Functions

def transform_geometry(geometry, transformer):
    """Transform geometry using a pyproj Transformer."""
    return transform(transformer.transform, geometry)


def adjust_longitude(x, y, z=None):
    """Adjust longitudes to be within [0, 360]."""
    if x < 0:
        x += 360
    return x, y


def load_and_transform_shapefile(shapefile_path):
    """Load the shapefile, transform geometries to WGS84, and adjust longitudes."""
    with fiona.open(shapefile_path, 'r') as shapefile:
        # Get CRS from source shapefile
        source_crs = shapefile.crs
        target_crs = CRS("EPSG:4326")  # Define target CRS as WGS84
        # Prepare transformer to convert source CRS to WGS84
        transformer = pyproj.Transformer.from_crs(
            source_crs, target_crs, always_xy=True
        )
        geometries = []
        for feature in shapefile:
            geometry = shape(feature["geometry"])
            transformed_geometry = transform(transformer.transform, geometry)
            adjusted_geometry = transform(adjust_longitude, transformed_geometry)
            ta_name = feature['properties'].get('TA2023_V_1', 'Unknown')
            climate = ta_to_climate_zone.get(ta_name, "Unknown")   
            geometries.append((adjusted_geometry, climate, ta_name))
        # Create GeoDataFrame
        gdf = gpd.GeoDataFrame(geometries, columns=['geometry', 'climate', 'ta_name'], crs=target_crs.to_string())
        return gdf


def split_geometry_by_line(geom, line, crs):
    split_result = split(geom, line)
    polygons = [geom for geom in split_result.geoms if isinstance(geom, (Polygon, MultiPolygon))]
    split_gdf = gpd.GeoDataFrame(geometry=polygons, crs=crs)
    split_gdf = split_gdf.to_crs("EPSG:2193")  # Convert to NZTM for area calculation
    split_gdf['area'] = split_gdf['geometry'].area
    split_gdf = split_gdf.to_crs(crs)  # Convert back for plotting
    if len(split_gdf) > 2:
        print(f"Warning: Splitting the geometry resulted in {len(split_gdf)} parts. Retaining the two largest.")
    elif len(split_gdf) < 2:
        print(f"Warning: Splitting the geometry resulted in {len(split_gdf)} parts.")
    split_gdf = split_gdf.sort_values('area', ascending=False)
    return split_gdf.head(2)


def plot_geometries(gdf, additional_features, title):
    """Plot the given list of Shapely geometries with climate zones, including river."""
    gdf = gdf[['geometry', 'climate', 'ta_name']]
    geometries = list(gdf.itertuples(index=False, name=None))
    _, ax = plt.subplots(figsize=(10, 10))
    climate_colors = {}
    unique_zones = sorted(set(zone for _, zone, _ in geometries))
    cmap = plt.get_cmap('tab20', len(unique_zones))
    for i, zone in enumerate(unique_zones):
        climate_colors[zone] = cmap(i)
    legend_labels = {}
    for geometry, climate, ta_name in geometries:
        fill_color = climate_colors[climate]
        if geometry.geom_type == 'Polygon':
            xs, ys = geometry.exterior.xy
            patch = ax.fill(xs, ys, alpha=0.5, fc=fill_color, edgecolor='black', label=ta_name)
        elif geometry.geom_type == 'MultiPolygon':
            for poly in geometry.geoms:
                xs, ys = poly.exterior.xy
                patch = ax.fill(xs, ys, alpha=0.5, fc=fill_color, edgecolor='black')
        if climate not in legend_labels:
            legend_labels[climate] = patch[0]
    for feature_name, feature_geometry in additional_features.items():
        if feature_geometry.geom_type == 'LineString':
            xs, ys = feature_geometry.xy
            ax.plot(xs, ys, color='blue', label=feature_name)
        elif feature_geometry.geom_type == 'MultiLineString':
            for line in feature_geometry.geoms:
                xs, ys = line.xy
                ax.plot(xs, ys, color='blue', label=feature_name)
    # Create custom legend
    ax.legend(legend_labels.values(), list(legend_labels.keys()) + list(additional_features.keys()))
    ax.set_title(title)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    plt.grid(True)


def ensure_empty_directory(directory):
    """Ensure that the specified directory is empty."""
    if os.path.exists(directory):
            shutil.rmtree(directory)
    os.makedirs(directory, exist_ok=True)


def main():
    ensure_empty_directory(OUTPUT_PATH)

    ta_gdf = load_and_transform_shapefile(SHAPEFILE_PATH)
    additional_features = {
        'Otekaieke River': OTEKAIEKE,
        'Rangitikei Split Line': RANGITIKEI_SPLIT_LINE
    }
    plot_geometries(ta_gdf, additional_features, 'Territorial Authority Boundaries with Approximate Climate Zones')
    plt.savefig(f'{OUTPUT_PATH}/1-territorial-authority-boundaries.png')

    # Split Waitaki District based on the Otekaieke River
    waitaki = ta_gdf[ta_gdf['ta_name'] == 'Waitaki District']
    waitaki_geom = waitaki['geometry'].iloc[0]
    split_waitaki = split_geometry_by_line(waitaki_geom, OTEKAIEKE, ta_gdf.crs)
    split_waitaki['centroid_lon'] = split_waitaki['geometry'].apply(lambda g: g.centroid.x)
    split_waitaki = split_waitaki.sort_values('centroid_lon')
    # Replace the original Waitaki District geometry with the sorted split geometries
    ta_gdf = ta_gdf[ta_gdf['ta_name'] != 'Waitaki District']
    new_entries = [
        {'geometry': split_waitaki.iloc[0]['geometry'], 'climate': 'Central Otago', 'ta_name': 'Waitaki District (Inland)'},
        {'geometry': split_waitaki.iloc[1]['geometry'], 'climate': 'Dunedin', 'ta_name': 'Waitaki District (Coastal)'}
    ]
    new_gdf = gpd.GeoDataFrame(new_entries, crs=ta_gdf.crs)
    ta_gdf = pd.concat([ta_gdf, new_gdf], ignore_index=True)

    # Split the Rangitikei District based on the Rangitikei Split Line (latitude)
    rangitikei = ta_gdf[ta_gdf['ta_name'] == 'Rangitikei District']
    rangitikei_geom = rangitikei['geometry'].iloc[0]
    split_rangitikei = split_geometry_by_line(rangitikei_geom, RANGITIKEI_SPLIT_LINE, ta_gdf.crs)
    split_rangitikei['centroid_lat'] = split_rangitikei['geometry'].apply(lambda g: g.centroid.y)
    split_rangitikei = split_rangitikei.sort_values('centroid_lat')
    # Replace the original Rangitikei District geometry with the sorted split geometries
    ta_gdf = ta_gdf[ta_gdf['ta_name'] != 'Rangitikei District']
    new_entries = [
        {'geometry': split_rangitikei.iloc[0]['geometry'], 'climate': 'Manawatu', 'ta_name': 'Rangitikei District (Coastal)'},
        {'geometry': split_rangitikei.iloc[1]['geometry'], 'climate': 'Taupo', 'ta_name': 'Rangitikei District (Inland)'}
    ]
    new_gdf = gpd.GeoDataFrame(new_entries, crs=ta_gdf.crs)
    ta_gdf = pd.concat([ta_gdf, new_gdf], ignore_index=True)
    plot_geometries(ta_gdf, additional_features, 'Territorial Authority Boundaries with Corrected Climate Zones')
    plt.savefig(f'{OUTPUT_PATH}/2-territorial-authority-boundaries-climate-zones.png')

    # Merge contiguous territorial authorities with the same climate zone
    merged_gdf = ta_gdf.dissolve(by='climate', aggfunc='first')
    merged_gdf.reset_index(inplace=True)
    plot_geometries(merged_gdf, additional_features, 'EECA-reconstructed NIWA Climate Zones')
    plt.savefig(f'{OUTPUT_PATH}/3-eeca-niwa-climate-zones.png')

    # Finally, save the merged geometries to a new shapefile
    merged_shapefile_path = f"{OUTPUT_PATH}/eeca_niwa_climate_boundaries/eeca_niwa_climate_boundaries.shp"
    ensure_empty_directory(f"{OUTPUT_PATH}/eeca_niwa_climate_boundaries/")
    merged_gdf.to_file(merged_shapefile_path)
    print(f"Saved merged climate zone boundaries to {merged_shapefile_path}")

    return merged_gdf


if __name__ == "__main__":
    merged_gdf = main()
