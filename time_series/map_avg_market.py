import pandas as pd
import matplotlib.pyplot as plt
import contextily as ctx
import numpy as np

for tag in ['cos', 'gak', 'dtw']:
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    cos_data = pd.read_csv(f'{tag}.csv')
    cos_coordinates = (cos_data['Longitude'], cos_data['Latitude'])
    cos_markets = cos_data['Market'].astype(int)  # 确保市场标签是整数型
    # 加载商场数据
    market_data = pd.read_csv('../market/stats.csv')  # 请确认文件路径正确
    market_coordinates = (market_data['经度'], market_data['纬度'])
    # 为每个商场和cos.csv中的散点创建颜色映射
    colors_tab20 = plt.get_cmap('tab20')
    market_colors = {i+1: colors_tab20(i % 20) for i in range(len(market_data))}
    # 根据市场编号分配颜色
    colors_cos = [market_colors[market] for market in cos_markets]
    # 绘制地图
    fig, ax = plt.subplots()
    # 绘制 cos.csv 数据，使得颜色与相应的商场匹配
    for market in np.unique(cos_markets):
        idx = cos_markets == market
        ax.scatter(cos_coordinates[0][idx], cos_coordinates[1][idx], color=market_colors[market], label=f'{market_data["名称"][market-1]}', s=1)

    for i, row in market_data.iterrows():
        ax.scatter(row['经度'], row['纬度'], color='red', edgecolor='black', s=70, marker='x', label=f'Market')

    ctx.add_basemap(ax, crs="EPSG:4326", source=ctx.providers.CartoDB.Positron)

    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), prop={'size': 8}, loc='lower right')
    plt.tight_layout()

    plt.savefig(f'map_{tag}', dpi=600, bbox_inches='tight')
    plt.show()
