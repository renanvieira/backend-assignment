import csv
import logging
import sys
import typing
from collections import defaultdict

logger = logging.getLogger(__name__)


class MalformedCSVFile(Exception):
    pass


def process_csv_files(
    barcodes: csv.DictReader, orders: csv.DictReader, output_path: str
):
    barcode_required_headers = ["barcode", "order_id"]
    order_required_headers = ["order_id", "customer_id"]

    if not barcodes.fieldnames:
        raise MalformedCSVFile(
            f"Barcode CSV is missing required columns: {barcode_required_headers}"
        )

    if not orders.fieldnames:
        raise MalformedCSVFile(
            f"Orders CSV is missing required columns: {order_required_headers}"
        )

    try:
        order_barcode_map, unused_barcodes = process_barcodes(barcodes)
        order_customer_map, top5_customers = process_orders(orders, order_barcode_map)
    except KeyError as err:
        raise MalformedCSVFile("CSV is not in the expected format") from err

    print("-------------------")
    print(f"- Unused Barcodes: {unused_barcodes}")
    print("-------------------")
    print("- TOP5 Customers:")
    print("customer_id,number_of_tickets")

    for k, v in top5_customers.items():
        print(f"{k},{v}")

    print("-------------------")
    with open(output_path, "w+") as fp:
        writer = csv.writer(fp)
        writer.writerow(["customer_id", "order_id", "barcodes"])
        for k, v in order_customer_map.items():
            writer.writerow([v["customer_id"], k, f"[{','.join(v['barcodes'])}]"])

    print(f"CSV file written to '{output_path}'")
    print("-------------------")


def process_orders(
    orders_csv: csv.DictReader, barcodes: dict[str, set[str]]
) -> tuple[dict[str, typing.Any], dict[str, int]]:

    seen = set()
    output: dict[str, typing.Any] = dict()
    ticket_counter: dict[str, int] = defaultdict(int)

    for row in orders_csv:
        order_id = row["order_id"]
        customer_id = row["customer_id"]
        order_barcodes = barcodes.get(order_id)

        if not order_barcodes:
            logger.error("Order Without Barcodes: %s", order_id)
            continue

        if order_id in seen:
            logger.error(
                "Duplicated order: '%s' from customer '%s'", order_id, customer_id
            )
            continue
        else:
            seen.add(order_id)

        output[order_id] = {"customer_id": customer_id, "barcodes": order_barcodes}
        ticket_counter[customer_id] += len(order_barcodes)

    sorted_ticket_counter = sorted(
        ticket_counter.items(), key=lambda item: (item[1], item[0]), reverse=True
    )

    top5_customers = dict(sorted_ticket_counter[:5])

    return (output, top5_customers)


def process_barcodes(dict_csv: csv.DictReader) -> tuple[dict[str, set[str]], int]:
    order_barcode = defaultdict(set)
    unused_barcodes = 0
    for row in dict_csv:
        barcode = row["barcode"]
        order_id = row["order_id"]

        if not order_id:
            unused_barcodes += 1
            continue

        if barcode in order_barcode[order_id]:
            logger.error("Duplicated barcode '%s' in order '%s'", barcode, order_id)
            continue

        order_barcode[order_id].add(barcode)

    return dict(order_barcode), unused_barcodes
