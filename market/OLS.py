import pandas as pd
import numpy as np
import statsmodels.api as sm

# 加载数据
communities_df = pd.read_csv('../data/statsv5.csv')

# 提取自变量和因变量
# X = communities_df[['MinDistance', 'BusinessStrength', 'CustomerFlow', 'DevelopmentPotential', 'SurroundingFacilities', 'TransactionCount', 'HousingTypeScore']]
# X = communities_df[['MinDistance', "westlake", 'TransactionCount', "HousingTypeScore"]].values
X = communities_df[['DC', "westlake", 'TransactionCount', "HousingTypeScore"]].values
y = communities_df['AvgPrice']

# 归一化自变量
X_normalized = (X - X.min()) / (X.max() - X.min())

# 添加截距项
X_normalized = sm.add_constant(X_normalized)

# 使用OLS模型拟合数据
model = sm.OLS(y, X_normalized).fit()

# 打印模型的摘要
print(model.summary())
