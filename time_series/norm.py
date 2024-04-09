import pandas as pd
from tqdm import tqdm

def normalize_row(row):
    max_val = row[date_columns].max()
    min_val = row[date_columns].min()
    normalized_values = (row[date_columns] - min_val) / (max_val - min_val)
    return normalized_values


df = pd.read_csv('statsv7.csv', encoding='utf-8-sig')
date_columns = [col for col in df.columns if '/' in col]
for index, row in tqdm(df.iterrows(), total=len(df), desc="Normalizing"):
    try:
        df.loc[index, date_columns] = normalize_row(row)
    except:
        df.drop(index, inplace=True)
df.to_csv('statsv8.csv', index=False, encoding='utf-8-sig')


df = pd.read_csv('market.csv', encoding='utf-8-sig')
date_columns = [col for col in df.columns if '/' in col]
for index, row in tqdm(df.iterrows(), total=len(df), desc="Normalizing"):
    try:
        df.loc[index, date_columns] = normalize_row(row)
    except:
        df.drop(index, inplace=True)
df.to_csv('marketv2.csv', index=False, encoding='utf-8-sig')
