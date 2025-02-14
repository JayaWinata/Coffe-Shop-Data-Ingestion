import os
import pandas as pd

def convert_to_csv(input_dir="/tmp/temp/", output_dir="/tmp/dataset/"):
    os.makedirs(output_dir, exist_ok=True)

    try:
        for file in os.listdir(input_dir):
            if file.endswith('.xlsx'):
                xlsx_path = os.path.join(input_dir, file)
                csv_file = os.path.join(output_dir, f"{os.path.splitext(file)[0]}.csv")

                print(f'Converting {xlsx_path} to {csv_file}')
                df = pd.read_excel(xlsx_path)
                df.to_csv(csv_file, index=False, encoding='utf-8')
                print(f"File converted successfully to: {csv_file}")

    except FileNotFoundError:
        print("Error: XLSX file not found")
    except Exception as e:
        print(f"Conversion error: {e}")

    return output_dir
