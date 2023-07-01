from datetime import datetime

import numpy as np
import pandas as pd

from library.FH_Hydrosat import FH_Hydrosat


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


def ndvi_from_collection(items, geom_point, tolerance, red_band, nir_band, 
                         name):
    assets = items[0].to_dict()['assets'].keys()
    if len(items) > 0 and 'surface_reflectance' in assets:
        res_full = FH_Hydrosat(items, asset='surface_reflectance')
        res_dt = res_full.datetime

        red_ts = res_full.point_time_series_from_items(
            geom_point, tol=tolerance, nproc=6, band=red_band)
        nir_ts = res_full.point_time_series_from_items(
            geom_point, tol=tolerance, nproc=6, band=nir_band)

        ndvi_ts = (
            (np.array(nir_ts) - np.array(red_ts)) 
            / (np.array(nir_ts) + np.array(red_ts))
        )
        ndvi_dt = res_dt

        ndvi_df = pd.DataFrame(
            {'ndvi': ndvi_ts,
             'datetime': pd.to_datetime(ndvi_dt)}).sort_values(by='datetime')
        ndvi_df.index = (
            pd.to_datetime(ndvi_df['datetime'].dt.strftime('%Y-%m-%d'))
        )

        ndvi_series = ndvi_df['ndvi'].astype('float')
        ndvi_series.name = name

        return ndvi_series