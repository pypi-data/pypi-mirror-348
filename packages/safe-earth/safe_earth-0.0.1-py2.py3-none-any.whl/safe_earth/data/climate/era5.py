from typing import Literal, List
import numpy as np
import pandas as pd
import xarray as xr
import zarr
import cfgrib
import gcsfs
import fsspec
from safe.data.climate import wb2_stores

# TODO: support more resolutions
# TODO: support user-defined variable selection
def get_era5(
        resolution: Literal['240x121'],
        time: slice = slice('2020-01-01T00', '2021-01-11T00'),
    ) -> xr.Dataset:
    '''
    Get ERA5 data from the WeatherBench 2 API, by default gets data for 2020
    plus 10 days to accommodate lead times up to 10 days.
    '''

    if not resolution in wb2_stores.era5:
        raise ValueError(f'Resolution {resolution} is not supported')
    else:
        store = wb2_stores.era5[resolution]

    era5 = xr.open_zarr(
        store,
        storage_options={"token": "anon"}, 
        consolidated=True
    )
    era5 = era5.sel(time=time)

    # TODO: support user-defined variable selection
    era5['T850'] = era5['temperature'].sel(level=850)
    era5['Z500'] = era5['geopotential'].sel(level=500)
    era5 = era5[['T850', 'Z500']]

    if resolution == '240x121':
        era5['latitude'] = np.round(era5['latitude'], 1)
        era5['longitude'] = np.round(era5['longitude'], 1)
        era5 = era5.assign_coords(longitude=(((era5.longitude + 180) % 360) - 180)) # TODO: will likely need to do this at all resolutions
    # TODO: support more resolutions

    return era5
