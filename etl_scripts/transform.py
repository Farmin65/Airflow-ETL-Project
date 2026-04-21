import pandas as pd
import logging
import os


def transform_data():
    raw_path = '/home/evgeniy/airflow/data/raw/sales_data_2026.csv'


staging_path = '/home/evgeniy/airflow/data/staging/sales_clean.csv'

df = pd.read_csv(raw_path)

df['price'] = df['price'].astype(str).str.replace('$', '', regex=False).astype(float)
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
df['order_date'].fillna(pd.Timestamp('today'), inplace=True)

df['total_amount'] = df['price'] * df['quantity']
df = df[df['quantity'] > 0]

logging.info(f"Saving cleaned data to {staging_path}")
os.makedirs(os.path.dirname(staging_path), exist_ok=True)
df.to_csv(staging_path, index=False)

return staging_path