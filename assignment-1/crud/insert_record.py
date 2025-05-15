import pandas as pd
from crud.read_data import read_data

def insert_record(file_path, record):
    df = read_data(file_path)
    df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    df.to_csv(file_path, index=False)
    print("Record inserted successfully.")