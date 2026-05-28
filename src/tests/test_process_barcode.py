import csv
import io

from process import process_barcodes


def test_process_barcode_with_correct_csv():
    csv_content = "barcode,order_id\n111,1\n222,1\n333,2"
    f = io.StringIO(csv_content)
    reader = csv.DictReader(f)

    mapping, unused = process_barcodes(reader)

    assert mapping == {"1": ["111", "222"], "2": ["333"]}
    assert unused == 0


def test_process_barcode_ignores_duplicates():
    csv_content = "barcode,order_id\n111,1\n111,2"
    f = io.StringIO(csv_content)
    reader = csv.DictReader(f)

    mapping, _ = process_barcodes(reader)

    assert mapping == {"1": ["111"]}
    assert "2" not in mapping


def test_process_barcode_counts_unused_correctly():
    csv_content = "barcode,order_id\n111,1\n222,\n333,"
    csv_content = "barcode,order_id\n111,1\n222,\n333,"  # Two unused
    f = io.StringIO(csv_content)
    reader = csv.DictReader(f)

    mapping, unused = process_barcodes(reader)

    assert mapping == {"1": ["111"]}
    assert unused == 2
