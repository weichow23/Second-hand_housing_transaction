import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the data
file_path = '../data/stats.csv'
data = pd.read_csv(file_path)

# Let's get an overview of the price distribution across all years first
year_columns = [col for col in data.columns if 'AvgPrice' in col]
price_data = data[year_columns]

# Summary statistics of the price data
price_stats = price_data.describe()

# Plotting boxplots for each year
plt.figure(figsize=(20,10))
sns.boxplot(data=price_data)
means = price_data.mean()
plt.plot(range(len(means)), means, marker='o', linestyle='-', color='red', label='Yearly Mean')
plt.title('Boxplot of Average Prices by Year with Means')
plt.ylabel('Price')
plt.xlabel('Year')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.savefig('analysis_1')
plt.show()

# Now, let's calculate the percentage of properties in different price ranges
# Now, let's calculate the percentage and absolute number of properties in different price ranges
bins = [0, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000]
price_ranges = pd.cut(price_data.values.flatten(), bins=bins)
price_range_counts = price_ranges.value_counts()
price_range_distribution = (price_range_counts / price_range_counts.sum()) * 100

# Plotting the price range distribution as a bar chart and annotating with the absolute numbers
plt.figure(figsize=(20,10))
bars = price_range_distribution.sort_index().plot(kind='bar')
plt.title('Distribution of Prices in Different Ranges')
plt.ylabel('Percentage')
plt.xlabel('Price Range')
plt.xticks(rotation=45)
plt.grid(True)

# Annotate with the absolute numbers
for bar in bars.patches:
    plt.annotate(format(bar.get_height(), '.2f'),
                 (bar.get_x() + bar.get_width() / 2,
                  bar.get_height()), ha='center', va='center',
                 size=10, xytext=(0, 8),
                 textcoords='offset points')
plt.savefig('analysis_2')
plt.show()


plt.figure(figsize=(10,8))
plt.pie(price_range_counts, labels=price_range_counts.index.categories, autopct='%1.1f%%', startangle=140)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title('Pie Chart of Price Range Distribution')
plt.savefig('analysis_3')
plt.show()


print(price_stats, price_range_distribution)
# price_stats.to_csv('price_stats.csv')

# 将数据重塑为堆叠柱状图需要的格式
# 我们将为每个价格区间创建一个DataFrame，每列代表一个年份，每行代表价格区间的计数
price_range_data = {}  # 用于存储每个价格区间的数据

# 对于每个价格区间，计算每年该区间的房产数量
for lower, upper in zip(bins[:-1], bins[1:]):
    range_mask = (price_data >= lower) & (price_data < upper)  # 创建一个遮罩，标识价格位于当前区间内的房产
    # 计算每年的计数，并存储到字典中
    price_range_data[f'({lower}, {upper}]'] = range_mask.sum()

# 将字典转换为DataFrame
stacked_data = pd.DataFrame(price_range_data, index=year_columns)

# 绘制堆叠柱状图
plt.figure(figsize=(20,10))
# 从底部堆叠起
bottom = np.zeros(len(year_columns))

for price_range, counts in stacked_data.items():
    plt.bar(year_columns, counts, bottom=bottom, label=price_range)
    # 更新下一个条形的底部位置
    bottom += counts

plt.title('Stacked Distribution of Prices in Different Ranges per Year')
plt.ylabel('Count')
plt.xlabel('Year')
plt.xticks(rotation=45)
plt.legend(title='Price Range')
plt.grid(True)
plt.savefig('analysis_4')
plt.show()



percentage_data = pd.DataFrame(index=bins[:-1])

for year in year_columns:
    # Bin the data for each year
    year_data_binned = pd.cut(price_data[year].values, bins=bins).value_counts()
    # Calculate the percentage contribution of each year within each bin
    percentage_data[year] = (year_data_binned / year_data_binned.sum()) * 100

# Plotting the stacked bar chart
plt.figure()
percentage_data.plot(kind='bar', stacked=True)
plt.title('Stacked Bar Chart of Price Ranges by Yearly Contribution')
plt.ylabel('Percentage Contribution')
plt.xlabel('Price Range')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend(title='Year', bbox_to_anchor=(0.65, 1), loc='upper left')
plt.savefig('analysis_5')
plt.show()