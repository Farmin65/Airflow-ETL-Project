from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/../etl_scripts'))

from extract import extract_data
from transform import transform_data
from load import load_data

default_args = {
    'owner': 'student',
    'depends_on_past': False,
    'start_date': datetime(2026, 4, 20),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='student_sales_etl_pipeline',
    default_args=default_args,
    description='ETL CSV -> Clean CSV -> SQLite',
    schedule='@daily',
    catchup=False,
    tags=['education', 'python', 'sqlite']
) as dag:

    prepare_env = BashOperator(
        task_id='prepare_environment',
        bash_command='mkdir -p /home/evgeniy/airflow/data/raw /home/evgeniy/airflow/data/staging /home/evgeniy/airflow/db'
    )

    extract = PythonOperator(
        task_id='extract_from_source',
        python_callable=extract_data,
        op_kwargs={'file_path': '/home/evgeniy/airflow/data/raw/sales_data_2026.csv'}
    )

    transform = PythonOperator(
        task_id='transform_and_cleanse',
        python_callable=transform_data
    )

    load = PythonOperator(
        task_id='load_to_sqlite',
        python_callable=load_data
    )

    verify = BashOperator(
        task_id='check_row_count',
        bash_command='sqlite3 /home/evgeniy/airflow/db/sales.db "SELECT COUNT(*) FROM cleaned_sales;"'
    )

    prepare_env >> extract >> transform >> load >> verify