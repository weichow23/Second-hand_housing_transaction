'''
配色：https://matplotlib.org/stable/users/explain/colors/colormaps.html
地图： https://contextily.readthedocs.io/en/latest/providers_deepdive.html
'''
import pandas as pd
import matplotlib.pyplot as plt
import contextily as ctx
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import osmnx as ox
# 加载房产数据
data = pd.read_csv('../data/stats.csv')
coordinates = (data['Longitude'], data['Latitude'])
average_prices = data['AveragePrice']

# 加载商场数据
market_data = pd.read_csv('../market/stats.csv')
market_coordinates = (market_data['经度'], market_data['纬度'])
market_scores = market_data['综合评分']

# 设置颜色映射 - 房产
norm_avg_prices = Normalize(vmin=average_prices.min(), vmax=average_prices.max())
cmap_avg_prices = plt.get_cmap('viridis')
colors_avg_prices = [cmap_avg_prices(norm_avg_prices(price)) for price in average_prices]

# 设置颜色映射 - 商场
norm_market_scores = Normalize(vmin=(market_scores.min())/4, vmax=market_scores.max())
cmap_market_scores = plt.get_cmap('Reds')
colors_market_scores = [cmap_market_scores(norm_market_scores(score)) for score in market_scores]

# 绘制地图
fig, ax = plt.subplots()

# 绘制房产数据
ax.scatter(coordinates[0], coordinates[1], c=colors_avg_prices, s=0.4)

# 绘制商场数据
ax.scatter(market_coordinates[0], market_coordinates[1], c=colors_market_scores, s=16, marker='x')  # 使用正方形标记商场位置


# ox.config(use_cache=True, log_console=True)
# west_lake = ox.geocode_to_gdf('西湖区, 杭州, 中国')
# gongshu = ox.geocode_to_gdf('拱墅区, 杭州, 中国')
# shangcheng = ox.geocode_to_gdf('上城区, 杭州, 中国')
# west_lake.plot(ax=ax, facecolor='none', edgecolor=plt.get_cmap('tab20')(0), linewidth=2)
# gongshu.plot(ax=ax, facecolor='none', edgecolor=plt.get_cmap('tab20')(1), linewidth=2)
# shangcheng.plot(ax=ax, facecolor='none', edgecolor=plt.get_cmap('tab20')(2), linewidth=2)
ctx.add_basemap(ax, crs="EPSG:4326", source=ctx.providers.CartoDB.Positron)

# 添加颜色条 - 房产，调整大小
sm_avg_prices = ScalarMappable(cmap=cmap_avg_prices, norm=norm_avg_prices)
sm_avg_prices.set_array([])
fig.colorbar(sm_avg_prices, ax=ax, orientation='vertical', label='Average Price', fraction=0.02, pad=0.04, shrink=0.5)

# 添加颜色条 - 商场，调整大小
# sm_market_scores = ScalarMappable(cmap=cmap_market_scores, norm=norm_market_scores)
# sm_market_scores.set_array([])
# fig.colorbar(sm_market_scores, ax=ax, orientation='vertical', label='Composite Score', fraction=0.02, pad=0.04, shrink=0.5)

plt.legend()
plt.savefig('map_avg_and_market', dpi=1000, bbox_inches='tight')
plt.show()
