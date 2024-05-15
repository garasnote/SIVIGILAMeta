import geopandas as gpd
from typing import Union

def reshape_fin(x: int) -> int:
    if x == 2:
        return 1
    else:
        return 0
    
def reshape_bool(x: int) -> int:
    if x == 2:
        return 0
    else:
        return 1

    
def calculate_center(df: gpd.GeoDataFrame) -> gpd.GeoSeries:
    original_crs = df.crs
    planar_crs = 'EPSG:3857'
    return df['geometry'].to_crs(planar_crs).centroid.to_crs(original_crs)


if __name__ == "__main__":
    pass