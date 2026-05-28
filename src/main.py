import argparse
import csv
import logging
import os
import sys

from process import process_csv_files

logger = logging.getLogger(__name__)


def setup_logging():
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.addFilter(lambda r: r.levelno < logging.WARNING)

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.WARNING)

    fmt = logging.Formatter("[%(asctime)s] [%(levelname)s]:  %(message)s")
    stdout_handler.setFormatter(fmt)
    stderr_handler.setFormatter(fmt)

    logging.root.setLevel(logging.INFO)
    logging.root.addHandler(stderr_handler)
    logging.root.addHandler(stdout_handler)


def main():
    setup_logging()

    parser = argparse.ArgumentParser(
        prog="Renan's Backend Assignment",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "barcode_csv",
        nargs="?",
        default="./data/barcodes.csv",
        help="path to barcode CSV",
    )
    parser.add_argument(
        "orders_csv", nargs="?", default="./data/orders.csv", help="path to order CSV"
    )
    parser.add_argument(
        "-o",
        "--output",
        default="./data/output.csv",
        help="File where the result will be written to.",
    )

    args = parser.parse_args()

    if os.path.exists(args.output):
        logger.warning("Path '%s' already exists, it will be replaced.", args.output)

    try:
        with (
            open(args.barcode_csv, "r") as barcode_handle,
            open(args.orders_csv) as orders_handle,
        ):
            barcodes = csv.DictReader(barcode_handle)
            orders = csv.DictReader(orders_handle)

            process_csv_files(barcodes, orders, args.output)
    except FileNotFoundError as e:
        logger.exception("Could not find file - %s", e.filename)
        sys.exit(1)
    except PermissionError as e:
        logger.exception("Permission Denied - %s", e.filename)
        sys.exit(1)
    except Exception:
        logger.exception("An unexpected error occurred.")
        sys.exit(1)


if __name__ == "__main__":
    main()
