import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 读取数据
data = pd.read_csv('../market/stats.csv')

# 提取日期范围
dates = pd.date_range(start='2019-03-01', end='2023-10-01', freq='MS')

# 提取营业额数据列
revenue_columns = [col for col in data.columns if col.startswith('20')]
revenue_data = data[revenue_columns]

# 设置图像大小
plt.figure(figsize=(10, 6))

# 绘制折线图
for index, row in data.iterrows():
    plt.plot(dates, row[revenue_columns].values, label=str(row['名称']))  # 将商场名称转换为字符串

# 设置横纵坐标标签
plt.xlabel('日期')
plt.ylabel('营业额 (万)')

# 设置图例
plt.legend()
plt.savefig('market_line')
plt.show()
