'''
配色：https://matplotlib.org/stable/users/explain/colors/colormaps.html
地图： https://contextily.readthedocs.io/en/latest/providers_deepdive.html
'''
import pandas as pd
import matplotlib.pyplot as plt
import contextily as ctx
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

# 读取数据
data = pd.read_csv('../data/stats.csv')
coordinates = (data['Longitude'], data['Latitude'])
average_prices = data['AveragePrice']

# 计算价格的颜色表示，这里我们使用归一化后的价格来映射颜色
norm = Normalize(vmin=average_prices.min(), vmax=average_prices.max())
cmap = plt.get_cmap('inferno')  # 使用viridis颜色映射
colors = [cmap(norm(price)) for price in average_prices]

# 绘制地图
fig, ax = plt.subplots()
ax.scatter(coordinates[0], coordinates[1] + 0.005, c=colors, s=0.5)  # s控制点的大小，调整为20

# 将经纬度转换为Web Mercator
ctx.add_basemap(ax, crs="EPSG:4326", source=ctx.providers.OpenStreetMap.Mapnik)

# 添加颜色条
sm = ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
fig.colorbar(sm, ax=ax, orientation='vertical', label='Average Price')

plt.savefig('map_avg', dpi=700, bbox_inches='tight')
plt.show()
