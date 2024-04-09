import csv
import random
from collections import defaultdict
import pandas as pd

def replace_second_last_digit(coord_str):
    longitude, latitude = coord_str.split(',')
    longitude = longitude[:-2] + str(random.randint(0, 9))
    latitude = latitude[:-2] + str(random.randint(0, 9))
    return f"{longitude},{latitude}"

def find_duplicate_coordinates(csv_file:str = "community_name_map_new_gaode_random.csv"):
    coordinate_counts = defaultdict(list)
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            coordinate = row['Coordinates']
            coordinate_counts[coordinate].append(row)

    modified_rows = []
    for coordinate, rows in coordinate_counts.items():
        if len(rows) > 1:
            print(f"Duplicate coordinates {coordinate}:")
            for row in rows:
                modified_row = row.copy()
                modified_row['Coordinates'] = replace_second_last_digit(coordinate)
                modified_rows.append(modified_row)
        else:
            modified_rows.extend(rows)

    with open('community_name_map_new_gaode_random.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = modified_rows[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(modified_rows)

def split_name():
    df = pd.read_csv('result.csv')
    df[['房源名称', '房源信息']] = df['房源'].str.split(' ', n=1, expand=True)
    df.drop('房源', axis=1, inplace=True)
    columns = ['房源名称', '房源信息'] + [col for col in df if col not in ['房源名称', '房源信息']]
    df = df[columns]
    df.to_csv('resultv2.csv', index=False, encoding='utf-8-sig')

def split_cor():
    # 读取 stats.csv 文件
    with open('stats.csv', mode='r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        # 跳过第一行，因为第一行是标题行
        next(reader)
        # 创建一个新的 CSV 文件 statsv2.csv
        with open('statsv2.csv', mode='w', newline='', encoding='utf-8-sig') as outfile:
            writer = csv.writer(outfile)
            # 写入新的标题行
            writer.writerow(
                ['District', 'Street', 'Community', 'Longitude', 'Latitude', 'AveragePrice', 'StdDeviationPrice',
                 'MaxPrice', 'MinPrice', '2013AvgPrice', '2014AvgPrice', '2015AvgPrice', '2016AvgPrice', '2017AvgPrice',
                 '2018AvgPrice', '2019AvgPrice', '2020AvgPrice', '2021AvgPrice', '2022AvgPrice'])
            # 遍历原始文件的每一行
            for row in reader:
                # 将 Coordinates 列按逗号分隔成经度和纬度
                coordinates = row[3].split(',')
                # 写入新的一行到 statsv2.csv
                writer.writerow(
                    [row[0], row[1], row[2], coordinates[0], coordinates[1], row[4], row[5], row[6], row[7], row[8],
                     row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17]])


if __name__ == "__main__":
    # find_duplicate_coordinates()
    split_cor()
