import pandas as pd
import numpy as np
from tslearn.metrics import gak, sigma_gak, dtw

# 定义计算余弦相似度的函数
def cosine_similarity(a, b):
    cos_sim = np.dot(a, b.T) / (np.linalg.norm(a, axis=1)[:, np.newaxis] * np.linalg.norm(b, axis=1))
    return cos_sim

# 定义使用全局对齐核（GAK）计算相似度的函数
def gak_similarity(a, b):
    sigma = sigma_gak(np.concatenate((a, b), axis=0))
    nrows, ncols = a.shape[0], b.shape[0]
    gak_sim_matrix = np.zeros((nrows, ncols))
    for i in range(nrows):
        for j in range(ncols):
            gak_sim_matrix[i, j] = gak(a[i:i+1], b[j:j+1], sigma=sigma)
    return gak_sim_matrix

# 定义使用DTW计算相似度矩阵的函数
def dtw_similarity(a, b):
    nrows, ncols = a.shape[0], b.shape[0]
    dtw_dist_matrix = np.zeros((nrows, ncols))
    for i in range(nrows):
        for j in range(ncols):
            dtw_dist_matrix[i, j] = dtw(a[i], b[j])
    return dtw_dist_matrix

# 加载 CSV 文件
stats_df = pd.read_csv('statsv8.csv', usecols=["2019/3/1", "2019/4/1", "2019/5/1", "2019/6/1", "2019/7/1", "2019/8/1", "2019/9/1",
                                               "2019/10/1", "2019/11/1", "2019/12/1", "2020/1/1", "2020/2/1", "2020/3/1", "2020/4/1",
                                               "2020/5/1", "2020/6/1", "2020/7/1", "2020/8/1", "2020/9/1", "2020/10/1", "2020/11/1",
                                               "2020/12/1", "2021/1/1", "2021/2/1", "2021/3/1", "2021/4/1", "2021/5/1", "2021/6/1",
                                               "2021/7/1", "2021/8/1", "2021/9/1", "2021/10/1", "2021/11/1", "2021/12/1", "2022/1/1",
                                               "2022/2/1", "2022/3/1", "2022/4/1", "2022/5/1", "2022/6/1", "2022/7/1", "2022/8/1",
                                               "2022/9/1"])
market_df = pd.read_csv('marketv2.csv', usecols=["2019/3/1", "2019/4/1", "2019/5/1", "2019/6/1", "2019/7/1", "2019/8/1", "2019/9/1",
                                                 "2019/10/1", "2019/11/1", "2019/12/1", "2020/1/1", "2020/2/1", "2020/3/1", "2020/4/1",
                                                 "2020/5/1", "2020/6/1", "2020/7/1", "2020/8/1", "2020/9/1", "2020/10/1", "2020/11/1",
                                                 "2020/12/1", "2021/1/1", "2021/2/1", "2021/3/1", "2021/4/1", "2021/5/1", "2021/6/1",
                                                 "2021/7/1", "2021/8/1", "2021/9/1", "2021/10/1", "2021/11/1", "2021/12/1", "2022/1/1",
                                                 "2022/2/1", "2022/3/1", "2022/4/1", "2022/5/1", "2022/6/1", "2022/7/1", "2022/8/1",
                                                 "2022/9/1"])

mode = 'dtw'

if mode == 'cos':
    similarity_matrix = cosine_similarity(stats_df.values, market_df.values)  # 余弦相似度
elif mode == 'gak':
    similarity_matrix = gak_similarity(stats_df.values, market_df.values)  # GAK 相似度
elif mode == 'dtw':
    similarity_matrix = dtw_similarity(stats_df.values, market_df.values)

max_index = similarity_matrix.argmax(axis=1)
stats_geo_df = pd.read_csv('statsv8.csv', usecols=["Longitude", "Latitude"])
result_df = pd.DataFrame(columns=["Market", "Longitude", "Latitude"])
for i, index in enumerate(max_index):
    market_index = index + 1

    longitude = stats_geo_df.loc[i, "Longitude"]
    latitude = stats_geo_df.loc[i, "Latitude"]

    result_df.loc[i] = [market_index, longitude, latitude]

result_df.to_csv(f'{mode}.csv', index=False)
