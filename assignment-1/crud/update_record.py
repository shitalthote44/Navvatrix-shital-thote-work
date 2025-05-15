from crud.read_data import read_data

def update_quantity(file_path, order_id, quantity):
    df = read_data(file_path)
    if order_id in df["OrderID"].values:
        df.loc[df["OrderID"] == order_id, "Quantity"] = quantity
        df.to_csv(file_path, index=False)
        print(f"OrderID {order_id} updated successfully.")
    else:
        print("OrderID not found.")