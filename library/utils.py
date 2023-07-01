from datetime import datetime

import pandas as pd


def read_ameriflux(data_path, header=0, na_values=[-9999]):
    """
    Reads a standard Ameriflux data file as csv.

    Converts timestamps to datetime, adjusts time to UTC, 
    drops NA values, and sets the start date as index.

    Parameters
    ----------
    data_path: str
        Full file path
    header: int
        Row in which header is found
    na_values: list
        List of null values for the dataset
    
    Returns
    -------
    DataFrame
        The dataset as a pandas DataFrame
    """
    # Read data if path exists
    try:
        df = pd.read_csv(data_path, header=header, na_values=na_values)
    except (FileNotFoundError):
        print(f'File at path {data_path} not found')

    # Save value column names
    value_cols = df.columns[2:]

    # Convert timestamp objects
    df['start'] = df['TIMESTAMP_START'].apply(
        lambda x: datetime.strptime(str(x), "%Y%m%d%H%M.0")
        )
    df['end'] = df['TIMESTAMP_END'].apply(
        lambda x: datetime.strptime(str(x), "%Y%m%d%H%M.0")
        )

    # Drop NA
    df = df.dropna(subset=value_cols, how='all')

    df = df.set_index('start')
    col_order = (['end', 'TIMESTAMP_START', 'TIMESTAMP_END'] 
                 + value_cols.to_list())
    df = df[col_order]

    return df
