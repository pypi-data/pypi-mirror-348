from pygeoboundaries_geolab import get_gdf
import geopandas as gpd

gdf = get_gdf('ALL', ['UNSDG-subregion', 'worldBankIncomeGroup', 'maxAreaSqKM'])
gdf = gdf.drop(['shapeISO'], axis=1)
gdf.to_csv('safe/data/strata/gdf_region_income.csv', index=False)
