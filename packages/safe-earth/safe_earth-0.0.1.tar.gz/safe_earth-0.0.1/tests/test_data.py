import pytest
import shapely
import geopandas as gpd

def test_antimeridian_coordinate_equivalence():
    gdf = gpd.read_file('safe/metadata/gdf_region_income.csv')
    pos_antimeridian = shapely.LineString([(180,-90),(180,90)])
    pos_intersects = gdf[gdf.geometry.intersects(positive_antimeridian)]
    neg_antimeridian = shapely.LineString([(-180,-90),(-180,90)])
    neg_intersects = gdf[gdf.geometry.intersects( negative_antimeridian)]
    assert (pos_intersects == neg_intersects).all().all()
