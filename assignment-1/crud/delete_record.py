from crud.read_data import read_data

def delete_record(file_path, order_id):
    df = read_data(file_path)
    if order_id in df["OrderID"].values:
        df = df[df["OrderID"] != order_id]
        df.to_csv(file_path, index=False)
        print(f"OrderID {order_id} deleted successfully.")
    else:
        print("OrderID not found.")