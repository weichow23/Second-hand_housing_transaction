import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体，以支持中文显示
plt.rcParams['axes.unicode_minus'] = False  # 使坐标轴能够显示负号

# 读取市场数据
market_data = pd.read_csv('marketv2.csv')

# 提取日期范围
dates = pd.date_range(start='2019-03-01', end='2022-09-01', freq='MS')

# 确保dates与需要的数据列相匹配
revenue_columns = [f"{date.year}/{date.month}/1" for date in dates]  # 构建与dates匹配的列名列表

# 设置图像大小
plt.figure(figsize=(10, 6))

# 绘制每个商场的营业额折线图
for index, row in market_data.iterrows():
    plt.plot(dates, row[revenue_columns].values, label=str(row['名称']))  # 将商场名称转换为字符串

# 读取统计数据文件
stats_data = pd.read_csv('statsv8.csv')

# 计算statsv8.csv中日期列的均值，确保只计算dates对应的列
mean_values = stats_data[revenue_columns].mean()

# 绘制均值线
plt.plot(dates, mean_values.values, label='均值', color='black', linewidth=2, linestyle='--')

# 设置横纵坐标标签
plt.xlabel('日期')
plt.ylabel('值')

# 设置图例
plt.legend()

# 保存并展示图表
plt.savefig('market_line_with_mean')
plt.show()
