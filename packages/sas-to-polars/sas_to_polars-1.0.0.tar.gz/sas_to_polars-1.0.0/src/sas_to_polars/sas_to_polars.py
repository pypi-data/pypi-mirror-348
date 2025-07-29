######################
#  IMPORT LIBRARIES  #
######################
import os
import pyreadstat # Read in SAS7BDAT files into Pandas DataFrames
import polars as pl # Converts data into (Polars) DataFrame for data processing
import time # Display the execution time of program
import multiprocessing as mp # Leverages multiple CPU cores to increase I/O time and efficiency
from typing import Optional, List
import inspect
import sys



def read_sas_chunk(filepath: str, offset: int, chunksize: int) -> pl.DataFrame:
    """
    Reads a chunk of rows from SAS7BDAT file. Helper function to fetch_sas_parallel.

    Args:
        filepath (str): The filepath to the SAS dataset (.sas7bdat) file that is being converted to a Polars DataFrame
        offset (int): The starting row for the read-in chunk relative to the data being read in. This is used to avoid overlapping of chunks,
        chunksize (int): The number of rows to process at one time, per chunk. 

    Returns:
        pl.DataFrame: A Polars DataFrame representing the read chunk.
    """

    pandas_df, _ = pyreadstat.read_sas7bdat(
        filename_path=filepath,
        row_offset=offset,
        row_limit=chunksize
    )

    return pl.from_pandas(pandas_df)

def validate_processes_count(num_processes: int) -> None:

    CPU_USAGE_WARNING_THRESHOLD = 0.75
    max_procs = mp.cpu_count()
    proc_thresh = int(CPU_USAGE_WARNING_THRESHOLD * max_procs)
    if num_processes > max_procs:
        raise ValueError(
            f"The specified number of processes ({num_processes}) exceeds the number of "
            f"available CPU cores ({max_procs}). Use a value between 2 and {max_procs}."
        )
        if num_processes > proc_thresh:
            print(
                    f"Warning: The number of processes specified ({num_processes}) is greater than "
                    f"{int(CPU_USAGE_WARNING_THRESHOLD * 100)}% of available CPU cores ({max_procs}).\n" 
                    "This may impact system responsiveness or performance."
            )
            response = input("Do you want to continue? [y/n]: ").strip().lower()
            if response not in ("y", "yes"):
                print("Aborting. Please specify a lower number of processes.")
                sys.exit(1)

def sas_to_polars(
    filepath: str,
    chunksize: Optional[int] = 10_000,
    processes: Optional[int] = mp.cpu_count() // 4,
    use_lazy: Optional[bool] = True,
    unordered: Optional[bool] = False
) -> pl.DataFrame:
    """
    Reads in a .sas7bdat file in parallel using multiple processes and returns a concatenated Polars DataFrame.

    Args:
        filepath (str): The filepath to the SAS dataset (.sas7bdat) file that is being converted to a Polars DataFrame
        chunksize (int, optional): The number of rows to process at one time, per chunk. Defaults to 10,000.
        processes (int, optional): The number of processes/CPU cores to use for parallel processing. Defaults to 1/4 of machines available CPU cores.
        use_lazy (bool, optional): Whether or not to use Polar's lazy loading. Defaults to True.
        unordered (bool, optional): Whether or not to process and read in chunk without regard to row order. Defaults to False.

    Returns:
        pl.DataFrame: A Polars DataFrame with the data from the SAS dataset. This may return an empty DataFrame if the SAS dataset is empty.
    """

    # Validate number of processes used to prevent excessive system overhead.
    validate_processes_count(num_processes=processes)

    # Validate input file before processing
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    if not filepath.endswith(".sas7bdat"):
        raise ValueError(f"Unsupported file type: {filepath}. Expected a .sas7bdat file.")

    # Read metadata only to determine total row count for parallel processing.
    _, meta = pyreadstat.read_sas7bdat(filepath, metadataonly=True)
    total_rows = meta.number_rows

    # Check whether inputted dataset is empty or not.
    if total_rows == 0:
        df, _ = pyreadstat.read_sas7bdat(filepath)
        print("Warning: SAS dataset was empty. Returning an empty Polars DataFrame.")
        return pl.from_pandas(df)

    # Build args tuples for read_sas_chunk helper function.
    args = [
        (filepath, start, min(chunksize, total_rows - start))
        for start in range(0, total_rows, chunksize)
    ]
 
    dfs: List[pl.DataFrame] = []
    with mp.Pool(processes=processes) as pool:
        if unordered:
            for df in pool.imap_unordered(read_sas_chunk, args, chunksize=1):
                dfs.append(df)
        else:
            dfs = pool.starmap(read_sas_chunk, args)

    # Only accept returned objects if they are a Polars DataFrame. 
    dfs = [df for df in dfs if isinstance(df, pl.DataFrame)]

    # Return empty DataFrame if no valid chunks were processed.
    if not dfs:
        print("Unable to successfully read in any of the data. Returning an empty Polars DataFrame.")
        return pl.DataFrame()

    # If use_lazy = True, apply lazy loading for memory optimization.
    if use_lazy:
        if hasattr(pl, "concat_lazy"): # check if current Polars version has concat_lazy method.
            lazy_df = pl.concat_lazy([df.lazy() for df in dfs])
        else:
            lazy_df = pl.concat([df.lazy() for df in dfs])
        return lazy_df.collect()

    return pl.concat(dfs)

