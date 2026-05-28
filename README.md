# Tiqets Backend Assignment: CSV Processor

A production-ready Python tool to process order and barcode datasets, generate customer voucher summaries, and provide business analytics (Top 5 customers and unused ticket counts).

## Features
- **One-to-Many Mapping**: Correctly handles multiple barcodes per order.
- **Validation**: Detects and logs duplicate barcodes and orders without barcodes to `stderr`.
- **Performance**: Optimized with $O(1)$ set lookups for large datasets.
- **Structured Logging**: Uses standard Python logging with split streams (INFO to `stdout`, ERROR to `stderr`).

---

## Getting Started

### Prerequisites
- [uv](https://github.com/astral-sh/uv) (Recommended) or Python 3.13+
- [Docker](https://www.docker.com/) (Optional)

### Installation (Local)
```bash
# Install dependencies and setup environment
uv sync
```

### Running the Script
#### 1. Using `uv` (Local)
```bash
# Run with default files (data/barcodes.csv and data/orders.csv)
uv run src/main.py

# Run with custom paths and specific output
uv run src/main.py my_barcodes.csv my_orders.csv --output ./data/result.csv
```

#### 2. Using Docker
```bash
# Build the image
docker build -t tiqets-assignment .

# Run and save results to local disk (Volume Mount)
docker run --rm -v "$(pwd)/data:/app/data" tiqets-assignment
```

---

## Documentation & Bonus Points
- **Testing**: Run `PYTHONPATH=src uv run pytest src/tests/` to verify business logic.
- **Data Model**: Relational schema and indexing strategies in [docs/data_model/schema.sql](docs/data_model/schema.sql).
- **Deployment**: Standard production deployment plan in [docs/deploy.md](docs/deploy.md).
