from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from tasks.download_unzip import download_and_unzip
from tasks.convert_to_csv import convert_to_csv

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 2, 14),
    'retries': 1
}

URL = "https://example.com/path/to/your/file.zip"

with DAG(
    'unzip_and_convert',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:

    task_download_unzip = PythonOperator(
        task_id='download_and_unzip',
        python_callable=download_and_unzip,
        op_kwargs={'url': URL}
    )

    task_convert_csv = PythonOperator(
        task_id='convert_to_csv',
        python_callable=convert_to_csv
    )

    task_download_unzip >> task_convert_csv
