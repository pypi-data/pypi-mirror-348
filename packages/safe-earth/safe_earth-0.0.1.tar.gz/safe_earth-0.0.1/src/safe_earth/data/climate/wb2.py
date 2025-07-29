from typing import List
import numpy as np
import xarray as xr
import zarr
import cfgrib
import gcsfs
import fsspec
from safe.data.climate import wb2_stores

# TODO: support user-defined variable selection
def get_wb2_preds(
        model_name: str,
        resolution: str,
        lead_times: List[np.timedelta64],
        time: slice = slice('2020-01-01', '2020-12-31')
    ) -> xr.Dataset:

    if not model_name in wb2_stores.models:
        raise ValueError(f'Model {model_name} not exposed through WB2 API, check data/wb2_stores.py')
    elif not resolution in wb2_stores.models[model_name]:
        raise ValueError(f'Resolution {resolution} not available for model {model_name}, check data/wb2_stores.py')

    ds = xr.open_zarr(wb2_stores.models[model_name][resolution])
    ds = ds.sel(time=time)

    # TODO: support user-defined variable selection
    ds['T850'] = ds['temperature'].sel(level=850)
    ds['Z500'] = ds['geopotential'].sel(level=500)
    ds = ds[['T850', 'Z500']]

    if resolution == '240x121':
        ds['latitude'] = np.round(ds['latitude'], 1) # TODO: generalize/remove if not 240x121
        ds['longitude'] = np.round(ds['longitude'], 1) # TODO: generalize/remove if not 240x121
        ds = ds.assign_coords(longitude=(((ds.longitude + 180) % 360) - 180)) # TODO: will likely need to do this at all resolutions
    # TODO: support more resolutions

    ds = ds.sel(prediction_timedelta=ds.prediction_timedelta.isin(lead_times))

    return ds
