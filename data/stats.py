import pandas as pd
import numpy as np

# 读取数据
result_df = pd.read_csv('resultv2.csv')
communities_df = pd.read_csv('community_name_map_new_gaodev2.csv')

# 将成交日期列转换为datetime类型
result_df['成交日期'] = pd.to_datetime(result_df['成交日期'])

# 准备额外的统计数据列
avg_prices = []
std_deviations = []  # 使用标准差
max_prices = []
min_prices = []

# 准备按年份的均价列
year_columns = {year: [] for year in range(2013, 2023)}  # 从2012到2024年

for community in communities_df['Community']:
    community_data = result_df[result_df['Communit'] == community]
    if community_data.empty:
        avg_prices.append(np.nan)
        std_deviations.append(0)  # 无记录时标准差设为0
        max_prices.append(np.nan)
        min_prices.append(np.nan)
        # 对于每个年份，如果没有数据，添加NaN
        for year in year_columns.keys():
            year_columns[year].append(np.nan)
    else:
        avg_price = community_data['均价（元）'].mean()
        std_deviation = community_data['均价（元）'].std(ddof=0)  # 修正为样本标准差
        max_price = community_data['均价（元）'].max()
        min_price = community_data['均价（元）'].min()

        avg_prices.append(avg_price)
        std_deviations.append(std_deviation if not np.isnan(std_deviation) else 0)
        max_prices.append(max_price)
        min_prices.append(min_price)

        # 计算每个年份的均价
        for year in year_columns.keys():
            yearly_data = community_data[community_data['成交日期'].dt.year == year]
            yearly_avg_price = yearly_data['均价（元）'].mean() if not yearly_data.empty else np.nan
            year_columns[year].append(yearly_avg_price if not np.isnan(yearly_avg_price) else 0)  # 无数据时填充0

# 添加计算的统计数据到communities_df
communities_df['AveragePrice'] = avg_prices
communities_df['StdDeviationPrice'] = std_deviations
communities_df['MaxPrice'] = max_prices
communities_df['MinPrice'] = min_prices

# 添加每年的均价
for year, prices in year_columns.items():
    communities_df[f'{year}AvgPrice'] = prices

communities_df.to_csv('stats.csv', index=False, encoding='utf-8-sig')
