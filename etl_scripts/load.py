import pandas as pd
import sqlite3
import logging
import os


def load_data():
    staging_path = '/home/evgeniy/airflow/data/staging/sales_clean.csv'
    db_path = '/home/evgeniy/airflow/db/sales.db'
    table_name = 'cleaned_sales'

    if not os.path.exists(staging_path):
        raise FileNotFoundError(f"{staging_path} not found")

    df = pd.read_csv(staging_path)

    logging.info(f"Writing to {db_path}")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()

    logging.info(f"Done, {len(df)} rows inserted")