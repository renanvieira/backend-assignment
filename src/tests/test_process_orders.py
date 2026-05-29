import csv
import io

from process import process_orders


def test_process_orders_with_correct_csv():
    csv_content = "order_id,customer_id\n1,10\n2,20"
    f = io.StringIO(csv_content)
    reader = csv.DictReader(f)
    barcode_map = {"1": {"B1"}, "2": {"B2"}}

    output, _ = process_orders(reader, barcode_map)

    assert output["1"] == {"customer_id": "10", "barcodes": {"B1"}}
    assert output["2"] == {"customer_id": "20", "barcodes": {"B2"}}


def test_process_orders_skips_invalid_orders():
    csv_content = "order_id,customer_id\n1,10\n2,20"
    f = io.StringIO(csv_content)
    reader = csv.DictReader(f)
    barcode_map = {"1": {"B1"}}

    output, _ = process_orders(reader, barcode_map)

    assert "1" in output
    assert "2" not in output


def test_process_orders_aggregates_top_customers():
    csv_content = "order_id,customer_id\n1,C1\n2,C2\n3,C3\n4,C4\n5,C5\n6,C6\n"
    f = io.StringIO(csv_content)
    reader = csv.DictReader(f)

    dummy_barcode_map = {
        "1": {f"B1_{i}" for i in range(10)},
        "2": {f"B2_{i}" for i in range(9)},
        "3": {f"B3_{i}" for i in range(8)},
        "4": {f"B4_{i}" for i in range(7)},
        "5": {f"B5_{i}" for i in range(6)},
        "6": {f"B6_{i}" for i in range(11)},
    }

    _, top5 = process_orders(reader, dummy_barcode_map)

    assert len(top5) == 5

    top5_items = list(top5.items())

    # Assert the top5 is correctly ordered
    assert top5_items[0][1] == 11
    assert top5_items[1][1] == 10
    assert top5_items[2][1] == 9
    assert top5_items[3][1] == 8
    assert top5_items[4][1] == 7

    assert "C5" not in top5
