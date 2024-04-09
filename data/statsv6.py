import pandas as pd

# 读取两个CSV文件
stastv5_df = pd.read_csv('statsv5_.csv', encoding='utf-8-sig')
stast_df = pd.read_csv('stats_.csv', encoding='utf-8-sig')

# 删除stastv5_df中的Coordinates列
stastv5_df.drop(columns=['Coordinates'], inplace=True)

duplicate_communities = stast_df[stast_df.duplicated(['Community'])]['Community'].unique()
print("重复的Community字段:", duplicate_communities)


# 将Longitude和Latitude添加到stastv5_df中，并根据Community匹配赋值
stastv5_df['Longitude'] = stastv5_df['Community'].map(stast_df.set_index('Community')['Longitude'])
stastv5_df['Latitude'] = stastv5_df['Community'].map(stast_df.set_index('Community')['Latitude'])

# 将修改后的stastv5_df保存为新的CSV文件
stastv5_df.to_csv('statsv6.csv', index=False, encoding='utf-8-sig')
