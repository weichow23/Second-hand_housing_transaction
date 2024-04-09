import pandas as pd
import matplotlib.pyplot as plt
import contextily as ctx
from matplotlib.cm import get_cmap
from matplotlib.colors import to_hex

# 确保中文显示正确
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
data = pd.read_csv('../data/stats.csv')
coordinates = (data['Longitude'], data['Latitude'])
streets = data['Street']

# 获取唯一街道列表
unique_streets = streets.unique()

# 创建颜色映射
cmap = get_cmap('tab20')
colors_dict = {street: to_hex(cmap(i % 20)) for i, street in enumerate(unique_streets)}

# 绘制地图
fig, ax = plt.subplots()
sc = ax.scatter(coordinates[0], coordinates[1] + 0.005, c=[colors_dict[street] for street in streets], s=2)

# 添加底图
ctx.add_basemap(ax, crs="EPSG:4326", source=ctx.providers.CartoDB.Positron)

# 添加图例
handles = [plt.Line2D([0], [0], marker='o', color='w', label=street,
                      markerfacecolor=colors_dict[street], markersize=3) for street in unique_streets]

legend = ax.legend(handles=handles, title='Street', loc='lower left', bbox_to_anchor=(1, 0),
                   frameon=True, fontsize='x-small', ncol=3)

plt.savefig('map_street.png', dpi=700, bbox_inches='tight')
plt.show()
