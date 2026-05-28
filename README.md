Tiqets Backend Assignment
----------

The script was developed using Python 3.13 but it should work with any version above 3.12.

## Running the script
There are two ways of running the script: 

### 1. Docker
Build the container:
```sh
$ docker build docker build -t tiqets-assignment .
```

Run the container and print the output file contents:
```sh
$ docker run --rm --entrypoint sh tiqets-assignment -c "python src/main.py --output ./data/output.csv && cat /app/data/output.csv"
```

### 2. `uv`

Make sure you have `uv` installed, if not follow the installation here: https://docs.astral.sh/uv/getting-started/installation/

Then sync `uv` dependencies
```sh
$ uv sync
```

Once dependencies are installed: 
```sh 
$ uv run src/main.py --output ./data/out.csv
```
(run with default arguments)

To see the help message use the `--help`:
```sh
$ uv run src/main.py --help                 
usage: Renan Backend Assignment [-h] -o OUTPUT [barcode_csv] [orders_csv]

positional arguments:
  barcode_csv          path to barcode CSV (default: ./data/barcodes.csv)
  orders_csv           path to order CSV (default: ./data/orders.csv)

options:
  -h, --help           show this help message and exit
  -o, --output OUTPUT  File where the result will be written to.
```

## Tests 
Tests are located on `./src/tests` and can be running using the command below:
```sh
uv run pytest
```

## Notes
- The `devenv.*` files are my local dev machine related and doesn't affect anything on the script running process.
- Tests focus on behaviour rather than code coverage.




