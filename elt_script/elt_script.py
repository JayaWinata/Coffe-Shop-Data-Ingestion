from sqlalchemy import create_engine
from time import time
import pandas as pd
import argparse
import requests
import gzip
import shutil
import os

def unzip(url: str):
    filename = url.split('/')[-1]
    try:
        print(f'Downloading {filename}')
        response = requests.get(url)
        response.raise_for_status()

        print(f'Writing {filename}')
        with open(filename, 'wb') as f:
            f.write(response.content)

        if os.path.splitext(filename)[1].lower() == ".zip":
            csv_name = ''.join(filename.split('.')[:-1])
            print(f'Extracting {filename}')
            with gzip.open(filename, 'rb') as f_in:
                with open('../dataset/' + csv_name, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
    except Exception:
        raise Exception('File Unzipping Error')

    print(f"File downloaded and extracted to: {os.getcwd()}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--url', help='url for the csv file')
    args = parser.parse_args()
    unzip(args)


