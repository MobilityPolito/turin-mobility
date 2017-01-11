import geopandas as gpd
import matplotlib.pyplot as plt

gdf = gpd.read_file("../SHAPE/Zonizzazione.dbf")\
        .to_crs({"init": "epsg:4326"})

gs = gdf["geometry"]
gs.plot()
plt.show()

cinemas = gpd.read_file("./DataSource/geoportale/dati_torino/cinema_geo.dbf")\
            .to_crs({"init": "epsg:4326"})
points = cinemas["geometry"]

for point in points.values:
    print point
    intersect = gdf.contains(point)
    print intersect[intersect == True]


