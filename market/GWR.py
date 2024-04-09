import pandas as pd
import numpy as np
from mgwr.gwr import GWR
from mgwr.sel_bw import Sel_BW
import matplotlib.pyplot as plt
import contextily as ctx

def draw_coef(n:int, title: str):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    fig, ax = plt.subplots()  # 使用subplots获取ax对象
    scatter = ax.scatter(coords[:, 0], coords[:, 1], c=gwr.params[:, n], cmap='inferno',
                         s=0.4)
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('系数')
    ax.set_xlabel('经度')
    ax.set_ylabel('纬度')
    ax.set_title(title)
    ctx.add_basemap(ax, crs="EPSG:4326", source=ctx.providers.CartoDB.Positron)
    plt.savefig(f'coef_{n}.png', dpi=600, bbox_inches='tight')
    plt.show()


communities_df = pd.read_csv('../data/statsv6.csv')

coords = communities_df[['Longitude', 'Latitude']].values
# 提取自变量和因变量
X = communities_df[['DC', "westlake", 'TransactionCount', "HousingTypeScore"]].values
X = np.hstack((np.ones((X.shape[0], 1)), X))  # 添加截距
y = communities_df['AvgPrice'].values.reshape((-1, 1))

X_normalized = X # (X - X.min()) / (X.max() - X.min())

# 选择带宽
bw = Sel_BW(coords, y, X_normalized, kernel='bisquare', fixed=False).search()
# 拟合GWR模型
gwr = GWR(coords, y, X_normalized, bw, kernel='bisquare', fixed=False).fit()
print(gwr.summary())

draw = True
if draw:
    draw_coef(1, '商场 系数')
    draw_coef(2, '西湖距离 系数')
    draw_coef(3, '交易次数 系数')
    draw_coef(4, '户型 系数')