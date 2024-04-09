import pandas as pd
import matplotlib.pyplot as plt
import contextily as ctx
import osmnx as ox
from matplotlib.cm import get_cmap
from matplotlib.colors import to_hex

# 确保中文显示正确
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
data = pd.read_csv('../data/stats.csv', encoding='utf-8-sig')
coordinates = (data['Longitude'], data['Latitude'])
streets = data['District']

# 获取唯一街道列表并创建颜色映射
cmap = get_cmap('tab20')
unique_streets = streets.unique()
colors_dict = {street: cmap(i % cmap.N) for i, street in enumerate(unique_streets)}

# 绘制数据点
fig, ax = plt.subplots(figsize=(10, 10))
sc = ax.scatter(coordinates[0], coordinates[1] + 0.005, c=[to_hex(colors_dict[street]) for street in streets], s=3)

# 计算边界并设置显示区域
margin = 0.01
xlim = [coordinates[0].min() - margin, coordinates[0].max() + margin]
ylim = [coordinates[1].min() - margin, coordinates[1].max() + margin]
ax.set_xlim(xlim)
ax.set_ylim(ylim)

# 获取特定区域的边界数据并绘制
ox.config(use_cache=True, log_console=True)
west_lake = ox.geocode_to_gdf('西湖区, 杭州, 中国')
gongshu = ox.geocode_to_gdf('拱墅区, 杭州, 中国')
shangcheng = ox.geocode_to_gdf('上城区, 杭州, 中国')
west_lake.plot(ax=ax, facecolor='none', edgecolor=colors_dict['西湖'], linewidth=2)
gongshu.plot(ax=ax, facecolor='none', edgecolor=colors_dict['拱墅'], linewidth=2)
shangcheng.plot(ax=ax, facecolor='none', edgecolor=colors_dict['上城'], linewidth=2)

# 添加底图
ctx.add_basemap(ax, crs="EPSG:4326", source=ctx.providers.CartoDB.Positron, zorder=-1)

# 添加图例
handles = [plt.Line2D([0], [0], marker='o', color='w', label=street,
                      markerfacecolor=to_hex(color), markersize=6) for street, color in colors_dict.items()]
legend = ax.legend(handles=handles, title='District', loc='lower left', bbox_to_anchor=(1, 0),
                   frameon=True, fontsize='x-small')  # 减小字体大小并设置为三列显示

plt.savefig('map_district.png', dpi=600, bbox_inches='tight')
plt.show()
