def get_hrrr_point_data(lat, lon, start, days):

    import pandas
    from herbie import FastHerbie
    lat = 42
    lon = -93.7
    start_date = "2020-04-01 00:00"

    # Create a range of dates
    DATES = pandas.date_range(
        start=start_date,
        periods=29,
        freq="1D",
    )

    # Define forecast lead time (or analysis).
    fxx = range(0, 1)

    # Make FastHerbie Object.
    FH = FastHerbie(DATES, model="hrrr", fxx=fxx)

    # Read a subset of the data with xarray.
    ds = FH.xarray("TMP:2 m", remove_grib=False)

    # Get value nearest single point
    ds_point = ds.herbie.nearest_points(points=(lon, lat))

    return (ds_point)
