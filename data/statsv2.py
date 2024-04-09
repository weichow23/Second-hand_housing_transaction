import pandas as pd
import numpy as np
from tqdm import tqdm
import re

# 读取数据
def time_data():
    result_df = pd.read_csv('resultv2.csv')
    communities_df = pd.read_csv('community_name_map_new_gaodev2.csv')

    # 将成交日期列转换为datetime类型
    result_df['成交日期'] = pd.to_datetime(result_df['成交日期'])

    # 准备额外的统计数据列
    avg_prices = []
    std_deviations = []  # 使用标准差
    max_prices = []
    min_prices = []

    # 准备按年月的均价列
    year_month_columns = {(year, month): [] for year in range(2013, 2023) for month in range(1, 13)}

    for community in tqdm(communities_df['Community'], desc='Processing Communities'):
        community_data = result_df[result_df['Communit'] == community]
        if community_data.empty:
            avg_prices.append(np.nan)
            std_deviations.append(0)  # 无记录时标准差设为0
            max_prices.append(np.nan)
            min_prices.append(np.nan)
            # 对于每个年月，如果没有数据，添加NaN
            for year_month in year_month_columns.keys():
                year_month_columns[year_month].append(np.nan)
        else:
            avg_price = community_data['均价（元）'].mean()
            std_deviation = community_data['均价（元）'].std(ddof=0)  # 修正为样本标准差
            max_price = community_data['均价（元）'].max()
            min_price = community_data['均价（元）'].min()

            avg_prices.append(avg_price)
            std_deviations.append(std_deviation if not np.isnan(std_deviation) else 0)
            max_prices.append(max_price)
            min_prices.append(min_price)

            # 计算每个年月的均价
            for year, month in year_month_columns.keys():
                monthly_data = community_data[(community_data['成交日期'].dt.year == year) & (community_data['成交日期'].dt.month == month)]
                monthly_avg_price = monthly_data['均价（元）'].mean() if not monthly_data.empty else np.nan
                year_month_columns[(year, month)].append(monthly_avg_price if not np.isnan(monthly_avg_price) else 0)  # 无数据时填充0

    # 添加计算的统计数据到communities_df
    communities_df['AvgPrice'] = avg_prices
    communities_df['StdPrice'] = std_deviations
    communities_df['MaxPrice'] = max_prices
    communities_df['MinPrice'] = min_prices

    # 添加每年月的均价
    for year_month, prices in year_month_columns.items():
        year, month = year_month
        communities_df[f'{year}-{month:02d}'] = prices

    communities_df.to_csv('statsv2.csv', index=False, encoding='utf-8-sig')


def calculate_distance(coord1, coord2):
    """
    Calculate the Euclidean distance between two points.
    """
    return np.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)


def add_market_distances():
    communities_df = pd.read_csv('statsv2.csv')

    market_df = pd.read_csv('../market/stats.csv')

    communities_df['Coordinates'] = communities_df['Coordinates'].apply(lambda x: tuple(map(float, x.split(','))))
    market_df['Coordinates'] = market_df.apply(lambda row: (row['经度'], row['纬度']), axis=1)

    for i in range(len(market_df)):
        market_coord = market_df.iloc[i]['Coordinates']
        column_name = f'Market{i + 1}Distance'
        communities_df[column_name] = communities_df['Coordinates'].apply(lambda x: calculate_distance(x, market_coord) * 1000)
    communities_df.to_csv('statsv3.csv', index=False, encoding='utf-8-sig')


def add_transaction_data():
    '''
    v4
    :return:
    '''
    # 读取数据
    communities_df = pd.read_csv('statsv3.csv', encoding='utf-8-sig')
    result_df = pd.read_csv('resultv2.csv', encoding='utf-8-sig')

    # 初始化新列
    communities_df['TransactionCount'] = 0
    communities_df['HousingTypeScore'] = 0.0

    # 预编译正则表达式以提高效率
    room_pattern = re.compile(r'(\d+)室')
    hall_pattern = re.compile(r'(\d+)厅')

    for index, row in tqdm(communities_df.iterrows(), total=communities_df.shape[0], desc='Processing Communities'):
        community_name = row['Community']
        # 获取当前小区的所有交易记录
        community_transactions = result_df[result_df['Communit'] == community_name]

        # 计算交易次数并更新
        transaction_count = len(community_transactions)
        communities_df.at[index, 'TransactionCount'] = transaction_count

        # 提取并计算户型分数
        housing_type_score = 0.0
        for _, transaction in community_transactions.iterrows():
            try:
                room_match = room_pattern.search(transaction['户型'])
                hall_match = hall_pattern.search(transaction['户型'])
                rooms = float(room_match.group(1)) * 0.33 if room_match else 0
                halls = float(hall_match.group(1)) * 1 if hall_match else 0

                housing_type_score += rooms + halls
                if transaction_count > 0:
                    communities_df.at[index, 'HousingTypeScore'] = housing_type_score / transaction_count
                else:
                    communities_df.at[index, 'HousingTypeScore'] = 2
            except:
                communities_df.at[index, 'HousingTypeScore'] = 2

    communities_df.to_csv('statsv4.csv', index=False, encoding='utf-8-sig')

def add_enhanced_market_features():
    # 读取数据
    communities_df = pd.read_csv('statsv4.csv', encoding='utf-8-sig')
    market_df = pd.read_csv('../market/stats.csv', encoding='utf-8-sig')
    westlake = (120.144455,30.246405)

    for metric in ["MinDistance", "CompositeScore", "BusinessStrength", "CustomerFlow",
                   "DevelopmentPotential", "SurroundingFacilities", "DC", 'westlake']:
        communities_df[metric] = np.nan

    for index, community in tqdm(communities_df.iterrows(), total=communities_df.shape[0], desc='Processing Communities'):
        distances = []
        for i, market in market_df.iterrows():
            distance = calculate_distance(eval(community['Coordinates']), (market['经度'], market['纬度']))
            distances.append(distance)
        # 找到最近商场的距离及其索引
        min_distance = min(distances)
        min_index = distances.index(min_distance)
        # 更新DataFrame
        communities_df.at[index, "MinDistance"] = min_distance
        communities_df.at[index, "CompositeScore"] = market_df.iloc[min_index]["综合评分"]
        communities_df.at[index, "BusinessStrength"] = market_df.iloc[min_index]["商业实力"]
        communities_df.at[index, "CustomerFlow"] = market_df.iloc[min_index]["客流热力"]
        communities_df.at[index, "DevelopmentPotential"] = market_df.iloc[min_index]["发展潜力"]
        communities_df.at[index, "SurroundingFacilities"] = market_df.iloc[min_index]["周边设施"]
        communities_df.at[index, "DC"] = market_df.iloc[min_index]["综合评分"]/min_distance  # 哈夫引力模型
        communities_df.at[index, "westlake"] = 1/calculate_distance(eval(community['Coordinates']), (westlake[0], westlake[1]))

    communities_df.to_csv('statsv5.csv', index=False, encoding='utf-8-sig')


if __name__ == "__main__":
    # add_market_distances()
    # add_transaction_data()
    add_enhanced_market_features()

