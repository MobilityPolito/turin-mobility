import geopandas as gpd
import matplotlib.pyplot as plt

gdf = gpd.read_file("../SHAPE/Zonizzazione.dbf")

gs = gdf["geometry"]
gs.plot()
plt.show()

#p1 = Point(.5,.5)
#p2 = Point(.5,1)
#p3 = Point(1,1)
#
#g1 = gpd.GeoSeries([p1,p2,p3])
#g2 = gpd.GeoSeries([p2,p3])
#
#g = gpd.GeoSeries([Polygon([(0,0), (0,2), (2,2), (2,0)])])
#
#g1.intersects(g) # Flags the first point as inside, even though all are.
#g2.intersects(g) # The second point gets picked up as inside (but not 3rd)