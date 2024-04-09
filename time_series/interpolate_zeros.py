import pandas as pd
import numpy as np

df = pd.read_csv('statsv6.csv', encoding='utf-8-sig')
date_columns = [col for col in df.columns if '/' in col]

def interpolate_zeros(row):
    values = row[date_columns].astype(float).values  # 确保值为浮点数

    valid_indices = np.where(values != 0)[0]
    valid_values = values[valid_indices]

    # 限制多项式的最高度数，例如最多使用3次多项式
    max_degree = 3
    degree = min(len(valid_indices) - 1, max_degree)

    # 确保有足够的点来拟合所需度数的多项式
    if degree >= 0 and len(valid_indices) > 1:  # 至少需要2个点来进行拟合
        try:
            # 显式转换索引和值为浮点数
            coefs = np.polyfit(valid_indices.astype(float), valid_values, degree)
            poly = np.poly1d(coefs)

            # 使用多项式模型进行插值
            interpolated_values = values.copy()
            zero_indices = np.where(values == 0)[0]
            interpolated_values[zero_indices] = poly(zero_indices.astype(float))

            # 检查是否有任何插值结果是负数
            if any(val <= 0 for val in interpolated_values):
                return None

            return interpolated_values
        except ValueError:
            return None
    else:
        return None


# 对每一行应用插值并更新DataFrame
for index, row in df.iterrows():
    interpolated_values = interpolate_zeros(row)
    if interpolated_values is not None:
        df.loc[index, date_columns] = interpolated_values
    else:
        # 如果插值失败或产生负值，删除该行
        df.drop(index, inplace=True)

df.to_csv('statsv7.csv', index=False, encoding='utf-8-sig')

print("Interpolation complete.")
