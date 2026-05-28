import csv
from dataclasses import dataclass
from pprint import pprint


@dataclass
class Output:
    customer_id: int
    order_id: int
    barcode: list[str]


def main():
    with (
        open("./data/barcodes.csv", "r") as barcode_handle,
        open("./data/orders.csv") as orders_handle,
    ):
        barcodes = csv.DictReader(barcode_handle)
        orders = csv.DictReader(orders_handle)

        start_parsing(barcodes, orders)


def start_parsing(barcodes: csv.DictReader, orders: csv.DictReader):
    output = dict()
    aux_orders = dict()
    for i in orders:
        aux_orders[i["order_id"]] = i["customer_id"]

    print(aux_orders)

    aux_barcodes = dict()
    for i in barcodes:
        aux_barcodes[i["order_id"]] = i["barcode"]

    print(aux_barcodes)
    print("---------------------------------")
    print()

    for k, v in aux_orders.items():
        barcode = aux_barcodes.get(k)

        if k not in output:
            if barcode:
                barcode_list = [barcode]
            else:
                barcode_list = []

            output[k] = {"customer_id": v, "barcodes": barcode_list}
        else:
            output[k] = {
                "customer_id": v,
                "barcodes": output[k]["barcodes"].append(barcode),
            }

    pprint(output)


if __name__ == "__main__":
    main()
