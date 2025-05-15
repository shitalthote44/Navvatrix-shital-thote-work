import argparse
from create_sample import create_sample_data
from crud.insert_record import insert_record
from crud.read_customer import read_customer_orders
from crud.update_record import update_quantity
from crud.delete_record import delete_record

FILE_PATH = "sales_data.csv"

create_sample_data(FILE_PATH)

parser = argparse.ArgumentParser(description="Sales Data CRUD CLI")
subparsers = parser.add_subparsers(dest="command")

# Create
create_parser = subparsers.add_parser("create")
create_parser.add_argument("--orderid", type=int, required=True)
create_parser.add_argument("--customer", required=True)
create_parser.add_argument("--product", required=True)
create_parser.add_argument("--quantity", type=int, required=True)
create_parser.add_argument("--price", type=float, required=True)

# Read
read_parser = subparsers.add_parser("read")
read_parser.add_argument("--customer", required=True)

# Update
update_parser = subparsers.add_parser("update")
update_parser.add_argument("--orderid", type=int, required=True)
update_parser.add_argument("--quantity", type=int, required=True)

# Delete
delete_parser = subparsers.add_parser("delete")
delete_parser.add_argument("--orderid", type=int, required=True)

args = parser.parse_args()

if args.command == "create":
    record = {
        "OrderID": args.orderid,
        "CustomerName": args.customer,
        "Product": args.product,
        "Quantity": args.quantity,
        "Price": args.price
    }
    insert_record(FILE_PATH, record)

elif args.command == "read":
    read_customer_orders(FILE_PATH, args.customer)

elif args.command == "update":
    update_quantity(FILE_PATH, args.orderid, args.quantity)

elif args.command == "delete":
    delete_record(FILE_PATH, args.orderid)

else:
    parser.print_help()