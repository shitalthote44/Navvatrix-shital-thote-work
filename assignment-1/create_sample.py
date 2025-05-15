import pandas as pd
import os

def create_sample_data(file_path):
    if not os.path.exists(file_path):
        sample_data = {
            "OrderID": [101, 102, 103],
            "CustomerName": ["Alice", "Bob", "Charlie"],
            "Product": ["Laptop", "Phone", "Tablet"],
            "Quantity": [1, 2, 1],
            "Price": [1000, 500, 300]
        }
        df = pd.DataFrame(sample_data)
        df.to_csv(file_path, index=False)