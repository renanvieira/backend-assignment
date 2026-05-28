import csv
import io

from process import process_orders


def test_process_orders_with_correct_csv():
    csv_content = "order_id,customer_id\n1,10\n2,20"
    f = io.StringIO(csv_content)
    reader = csv.DictReader(f)
    barcode_map = {"1": ["B1"], "2": ["B2"]}

    output, _ = process_orders(reader, barcode_map)

    assert output["1"] == {"customer_id": "10", "barcodes": ["B1"]}
    assert output["2"] == {"customer_id": "20", "barcodes": ["B2"]}


def test_process_orders_skips_invalid_orders():
    csv_content = "order_id,customer_id\n1,10\n2,20"
    f = io.StringIO(csv_content)
    reader = csv.DictReader(f)
    barcode_map = {"1": ["B1"]}

    output, _ = process_orders(reader, barcode_map)

    assert "1" in output
    assert "2" not in output


def test_process_orders_aggregates_top_customers():
    csv_content = "order_id,customer_id\n1,10\n2,10\n3,20"
    f = io.StringIO(csv_content)
    reader = csv.DictReader(f)
    barcode_map = {"1": ["B1", "B2"], "2": ["B3"], "3": ["B4"]}

    _, top5 = process_orders(reader, barcode_map)

    assert top5["10"] == 3
    assert top5["20"] == 1
