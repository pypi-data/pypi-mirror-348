import pytest
import polars as pl
from sas_to_polars import sas_to_polars, validate_processes_count
import os
import multiprocessing as mp

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "test_data")

def test_valid_process_count():
    validate_processes_count(2)

def test_too_many_process_raises():
    with pytest.raises(ValueError):
        validate_processes_count(mp.cpu_count() + 1)

def test_conversion_success():
    filepath = os.path.join(TEST_DATA_DIR, "valid_data.sas7bdat")
    result = sas_to_polars(filepath)
    assert result is not None
    assert isinstance(result, pl.DataFrame)
    assert len(result) > 0

def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        sas_to_polars("non_existent.sas7bdat")

def test_wrong_file_extension():
    filepath = os.path.join(TEST_DATA_DIR, "bad_file.csv")
    with pytest.raises(ValueError):
        sas_to_polars(filepath)

def test_conversion_empty_file():
    filepath = os.path.join(TEST_DATA_DIR, "empty_data.sas7bdat")
    result = sas_to_polars(filepath)
    assert result is not None
    assert len(result) == 0
