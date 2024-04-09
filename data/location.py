'''
用于查找对应的经纬度
'''
import pandas as pd
import requests

def tengxun():
    df = pd.read_csv('community_name_map.csv')
    url_template = "https://apis.map.qq.com/ws/geocoder/v1/?address={}&key=PVJBZ-YY7LL-5G3PP-EE4JT-62SY5-CLBLB"

    index = 0
    while index < len(df):
        # 只处理flagC未标记的行
        if pd.isna(df.at[index, 'flagC']) or df.at[index, 'flagC'] != 1:
            # 构建查询字符串
            query_address = f"杭州市{df.at[index, 'Street']}{df.at[index, 'Community']}"
            # 发送请求
            response = requests.get(url_template.format(query_address))
            data = response.json()
            print(data)
            # 检查响应状态
            if data['status'] == 0:
            # if data['status'] == 0 and data['result']['title'] == df.at[index, 'Community']:
                location = data['result']['location']
                # 更新DataFrame
                df.at[index, 'Coordinates'] = f"{location['lng']},{location['lat']}"
                df.at[index, 'flagC'] = 1
                # 将修改写入CSV文件
                df.to_csv('community_name_map_updated_oringal.csv', index=False, encoding='utf-8-sig')
        index += 1

def gaode():
    df = pd.read_csv('community_name_map_new_gaode.csv')
    # 高德地图API的Key，需要替换成你自己的Key
    api_key = "ab89b014a3b938288bca8325d5c697d2"
    url_template = "https://restapi.amap.com/v3/geocode/geo?address={}&key={}"

    index = 0
    while index < len(df):
        # 只处理flagC未标记的行
        if pd.isna(df.at[index, 'flagC']) or df.at[index, 'flagC'] != 1:
            # 构建查询字符串
            query_address = f"杭州市{df.at[index, 'Street']}{df.at[index, 'Community']}"
            # 发送请求
            response = requests.get(url_template.format(query_address, api_key))
            data = response.json()
            print(data)
            # 检查响应状态
            if data['status'] == '1' and data['count'] != '0':
                # 高德地图可能返回多个结果，这里我们取第一个结果
                location = data['geocodes'][0]['location'].split(',')
                # 更新DataFrame
                df.at[index, 'Coordinates'] = f"{location[0]},{location[1]}"
                df.at[index, 'flagC'] = 1
                # 将修改写入CSV文件
                df.to_csv('community_name_map_new_gaode_updated.csv', index=False, encoding='utf-8-sig')
        index += 1

if __name__ == "__main__":
    gaode()