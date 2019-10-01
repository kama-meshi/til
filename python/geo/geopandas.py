###############################################################################
# GeoPandas
###############################################################################
# ポリゴンの一覧から対象のポイントを含むポリゴンを取得する。
import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon, Point
import numpy as np
# 依存パッケージ（Cartopy）のインストールにエラーとなるため下記でインストールを行う
# pip install git+https://github.com/SciTools/cartopy
# pip install contextily
import contextily as ctx

# 標準地域メッシュ（1次メッシュ）
lats = np.arange(20, 40, (2 / 3))
lons = np.arange(120, 140, dtype='f8')


def polygon(x, y):
    x1 = x
    y1 = y
    x2 = x + (2 / 3)
    y2 = y + 1
    return Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)])


ufunc = np.frompyfunc(polygon, 2, 1)
mesh = np.stack(np.meshgrid(lats, lons, indexing='ij'), -1).reshape(-1, 2)
polygons = ufunc(mesh[:, 0], mesh[:, 1])
attr = np.tile([0, 1, 2, 3, 4], 120)
df = pd.DataFrame(np.column_stack((polygons, attr)),
                  columns=['mesh', 'value'])
gdf = gpd.GeoDataFrame(df, geometry='mesh')

tokyo_tower = Point(35.658581, 139.745433)
tokyo_tower_mesh = gdf[gdf.contains(tokyo_tower)]
tokyo_tower_mesh.iloc[0]['value']
