import os
import requests
import zipfile

def download_and_unzip(url, output_dir="/tmp/temp/"):
    filename = url.split('/')[-1]
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)

    try:
        print(f'Downloading {filename}')
        response = requests.get(url)
        response.raise_for_status()

        with open(output_path, 'wb') as f:
            f.write(response.content)

        print(f'Extracting {output_path}')
        with zipfile.ZipFile(output_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)

    except requests.exceptions.RequestException as e:
        raise Exception(f'File Download Error: {e}')
    except zipfile.BadZipFile as e:
        raise Exception(f'Invalid zip file: {e}')
    except Exception as e:
        raise Exception(f'File Unzipping Error: {e}')

    print(f"File downloaded and extracted to: {os.path.abspath(output_dir)}")
    return output_dir
