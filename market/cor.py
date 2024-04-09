import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

communities_df = pd.read_csv('../data/statsv5.csv')

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
corr_matrix = communities_df[["westlake", 'MinDistance', 'CompositeScore', 'BusinessStrength', 'CustomerFlow', 'DevelopmentPotential', 'SurroundingFacilities', 'TransactionCount', 'HousingTypeScore']].corr()
plt.figure(figsize=(10, 8))  # 设置图形的大小
sns.heatmap(corr_matrix, annot=True, cmap='viridis', fmt='.2f')
plt.title('相关性热力图')
plt.savefig('cor')