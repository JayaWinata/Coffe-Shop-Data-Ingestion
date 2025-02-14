from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from elt_script.download_and_unzip import download_and_unzip
from elt_script.remove_csv import remove_csv
from elt_script.convert_to_csv import convert_to_csv

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 2, 14),
    'retries': 1
}

URL = "https://www.kaggle.com/api/v1/datasets/download/ahmedabbas757/coffee-sales"
FILENAME = URL.split('/')[-1]
CSV_FILE_PATH = f"/tmp/dataset/{FILENAME}.csv"

with DAG(
    'unzip_and_convert',
    default_args=default_args,
    schedule_interval='@daily',
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

    task_remove_csv >> task_download_unzip >> task_convert_csv
