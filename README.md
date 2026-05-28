# Tiqets Backend Assignment

A Python script to process order and barcode csv files.

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
# Run with default files (data/barcodes.csv and data/orders.csv) and default output (data/output.csv)
uv run src/main.py

# Run with custom paths and specific output
uv run src/main.py my_barcodes.csv my_orders.csv --output ./data/result.csv
```

You can use `--help` to see all the arguments of the script.
```bash
$ uv run src/main.py --help
usage: Renan's Backend Assignment [-h] [-o OUTPUT] [barcode_csv] [orders_csv]

positional arguments:
  barcode_csv          path to barcode CSV (default: ./data/barcodes.csv)
  orders_csv           path to order CSV (default: ./data/orders.csv)

options:
  -h, --help           show this help message and exit
  -o, --output OUTPUT  File where the result will be written to. (default: ./data/output.csv)
```


#### 2. Using Docker
```bash
# Build the image
docker build -t tiqets-assignment .

# Run and save results to local temporary folder (replace the /tmp/backend_assignment with you preferred path).
docker run --rm -v "/tmp/backend_assignment/data:/app/data" tiqets-assignment
```

---

## Testing
The project uses `pytest` for testing.
```bash
uv run pytest src/tests/
```

---
# Deployment Plan

**Docker Build:**
```bash
docker build -t tiqets-assignment .
```
Once image is build it can be deployed on any containarized environment.
If needed to run on a VM/baremetal infrastructure, we can follow the same steps inside the Dockerfile to setup the script.

**Scheduling:**
Run via Cron or Systemd Timer. Alternatevily, the docker image can be used by an orchestrator with scheduling (k8s cronjob, AWS ECS).
Another option, is refactoring the main.py to use Celery with Beat to have a consistent scheduling or react from messages on a queue.

**Monitoring**
- The script exits with code `1` on failure; All errors are logged to `stderr`, which makes log collection easier for monitoring tools like APMs.

---
# Data Model

!(Entity Relatioship Diagram)[./docs/data_model/schema.png)

## DDL
```sql
CREATE TABLE customers (
    id INT PRIMARY KEY,
    -- In a real system, we would have name, email, etc.
    email VARCHAR(255) UNIQUE
);

CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE barcodes (
    barcode VARCHAR(255) PRIMARY KEY,
    order_id INT UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_order FOREIGN KEY (order_id) REFERENCES orders(id)
);

CREATE INDEX idx_orders_customer_id ON orders(customer_id);
```




# AI Disclaimer
- Polish documentation
- Explore edge cases not covered by tests

