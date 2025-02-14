import pandas as pd
import requests
import argparse
import zipfile
import shutil
import stat
import gzip
import os


def unzip(args):
    url = args.url
    filename = url.split('/')[-1]
    output_dir = "../temp/"
    os.makedirs(output_dir, exist_ok=True)
    output_path = output_dir + filename
    try:
        print(f'Downloading {filename}')
        response = requests.get(url)
        response.raise_for_status()

        print(f'Writing {filename}')
        with open(output_dir + filename, 'wb') as f:
            f.write(response.content)

        print(f'Extracting {output_path}')
        with zipfile.ZipFile(output_path, 'r') as zip_ref:
            for file_info in zip_ref.infolist():
                extracted_filename = file_info.filename
                # if extracted_filename.lower().endswith(('.csv', '.CSV')):
                with zip_ref.open(file_info) as f_in:
                    output_path = os.path.join(output_dir, extracted_filename)
                    with open(output_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)

    except requests.exceptions.RequestException as e:
        raise Exception(f'File Download Error: {e}')
    except zipfile.BadZipFile as e:
        raise Exception(f'Invalid zip file: {e}')
    except Exception as e:
        raise Exception(f'File Unzipping Error: {e}')

    print(f"File downloaded and extracted to: {os.path.abspath(output_dir)}")

    try:
        csv_path = "../dataset"
        os.makedirs(csv_path, exist_ok=True)
        csv_path = f"../dataset/{filename}.csv"

        print(f'Converting file to {csv_path}')
        df = pd.read_excel(output_path)
        df.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"File converted successfully to: {csv_path}")
    except FileNotFoundError:
        print(f"Error: XLSX file not found at {output_path}")
    except Exception as e:
        print(f"An error occurred during conversion: {e}")

    print(f"File converted to: {os.path.abspath(csv_path)}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download and extract zip or gz file')
    parser.add_argument('--url', help='URL for the zip or gz file')
    args = parser.parse_args()
    unzip(args)