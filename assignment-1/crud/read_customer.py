from crud.read_data import read_data

def read_customer_orders(file_path, customer_name):
    df = read_data(file_path)
    customer_df = df[df["CustomerName"] == customer_name]
    print(f"\n Orders placed by {customer_name}:\n", customer_df)
