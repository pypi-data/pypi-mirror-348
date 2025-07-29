# sas_to_polars

A light Python package for converting and processing SAS datasets (.sas7bdat files) into a Polars DataFrame. Designed for high-performance data transformation by leveraging parallel computing.

---

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)

---

## Overview

This package provides a fast and convenient way to read SAS datasets into Polars DataFrames. Converting SAS datasets in Python often requires specific libraries. For large datasets, the conversion process can be a bottleneck. This package addresses this by leveraging concurrent programming to speed up the conversion.

`sas_to_polars` allows users to quickly transform their SAS data into the efficient Polars DataFrame structure for further analysis and manipulation in Python.

---

## Installation

This package requires Python 3.8 or higher.

The following Python libraries are necessary and will be installed as dependencies:

- `pyreadstat`: For reading SAS datasets.
- `polars`: For high-performance data manipulation.
- `pyarrow`: For efficient data conversion (required by Polars).

You can install `sas_to_polars` using pip:

```bash
pip install sas-to-polars  # Replace with your actual package name on PyPI
```

After running this command, pip will resolve and install the required dependencies (pyreadstat and polars) along with your sas_to_polars package.

To verify the installation, you can run:
`python -c "import sas_to_polars`

If no output is returned, the installation was successful.

---

## Usage

The primary function in this package is sas_to_polars. Here's how to use it.

```python
from sas_to_polars import sas_to_polars

df = sas_to_polars(filepath="path/to/dataset/data.sas7bdat")
print(df.head())
```

The `sas_to_polars` function accepts the following optional parameters:

- chunksize: int = 10_000: The number of rows to read in each chunk during parallel processing.
- processes: int = mp.cpu_count() // 4: The number of parallel processes to use for conversion. Defaults to a quarter of the available CPU cores.
- use_lazy: bool = True: Whether to use Polars lazy loading for potentially more efficient out-of-memory operations.
- unordered: bool = False: Whether to maintain the original order of columns from the SAS dataset.

For more detailed information about the sas_to_polars function and its parameters, you can use Python's built-in help function:

```python
help(sas_to_polars)
```

---

### Example Dataset Output

```text
Shape: (3, 3)
┌─────┬─────────┬──────┐
│ id  ┆ name    ┆ age  │
│ --- ┆ ---     ┆ ---  │
│ f64 ┆ str     ┆ f64  │
╞═════╪═════════╪══════╡
│ 1.0 ┆ Alice   ┆ 30.0 │
│ 2.0 ┆ Bob     ┆ 35.0 │
│ 3.0 ┆ Charlie ┆ 40.0 │
└─────┴─────────┴──────┘
```
---

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
