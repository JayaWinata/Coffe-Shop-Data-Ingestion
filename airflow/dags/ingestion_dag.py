from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
import sys

sys.path.append('/opt')
from ingestion_script.download_and_unzip import download_and_unzip
from ingestion_script.remove_csv import remove_csv
from ingestion_script.convert_to_csv import convert_to_csv

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 2, 14),
    'retries': 1
}

URL = "https://www.kaggle.com/api/v1/datasets/download/ahmedabbas757/coffee-sales"
FILENAME = URL.split('/')[-1] + ".csv"
CSV_FILE_PATH = f"/tmp/dataset/{FILENAME}"

CLICKHOUSE_IMAGE_NAME = 'clickhouse_db'
DB_NAME = 'coffee_shop'
TABLE_NAME = 'sales'

with DAG(
    dag_id='data_ingestion',
    default_args=default_args,
    schedule_interval="0 0 * * 0",
    start_date=datetime(2024,2,13),
    catchup=False
) as dag:

    task_remove_csv = PythonOperator(
        task_id='remove_csv',
        python_callable=remove_csv,
        op_kwargs={'file_path': CSV_FILE_PATH}
    )

    task_download_unzip = PythonOperator(
        task_id='download_and_unzip',
        python_callable=download_and_unzip,
        op_kwargs={'url': URL}
    )

    task_convert_csv = PythonOperator(
        task_id='convert_to_csv',
        python_callable=convert_to_csv
    )

    task_load_to_clickhouse = BashOperator(
        task_id='load_csv_to_clickhouse',
        bash_command=f"""
        docker exec {CLICKHOUSE_IMAGE_NAME} clickhouse-client -u admin --password password -q "
        DROP DATABASE IF EXISTS {DB_NAME};
        CREATE DATABASE IF NOT EXISTS {DB_NAME};
        CREATE TABLE IF NOT EXISTS {DB_NAME}.{TABLE_NAME} ENGINE = MergeTree()
        PRIMARY KEY (\`transaction_date\`, \`store_id\`, \`product_id\`)
        ORDER BY (\`transaction_date\`, \`store_id\`, \`product_id\`)
        SETTINGS allow_nullable_key = 1
        AS SELECT * FROM file('{FILENAME}', 'CSVWithNames');
        "
        """,
        dag=dag
    )

    task_remove_csv >> task_download_unzip >> task_convert_csv >> task_load_to_clickhouse
