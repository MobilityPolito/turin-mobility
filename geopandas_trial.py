import geopandas as gpd

gdf = gpd.read_file("../dati_torino/zonestat_popolazione_residente_2015_geo.dbf")\
        .to_crs({"init": "epsg:4326"})

