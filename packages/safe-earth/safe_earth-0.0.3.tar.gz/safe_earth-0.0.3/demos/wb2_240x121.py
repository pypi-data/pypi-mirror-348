import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import safe.data.climate.era5
import safe.data.climate.wb2
import safe.metrics.losses
import safe.metrics.errors
import pandas as pd
import numpy as np
import pickle
import time
import pdb
import platform

models = ['graphcast', 'keisler', 'pangu', 'sphericalcnn', 'fuxi', 'neuralgcm']
resolution = '240x121'
lead_times = [np.timedelta64(x, 'h') for x in range(12, 241, 12)]
era5 = safe.data.climate.era5.get_era5(resolution)
data = []
for model_name in models:
    preds = safe.data.climate.wb2.get_wb2_preds(model_name, resolution, lead_times)
    loss_gdf = safe.metrics.losses.climate_weighted_l2(
        data=preds, 
        ground_truth=era5, 
        lon_dim='longitude', 
        lat_dim='latitude',
        lead_time_dim='prediction_timedelta',
        reduction_dims=['time'],
        use_polygons=True,
        polygon_edge_in_degrees=1.5,
    )
    metrics = safe.metrics.errors.stratified_rmse(
        loss_gdf,
        loss_metrics=['weighted_l2'],
        strata_groups='all',
        added_cols={'model': model_name}
    )
    data.append(metrics)
safe.viz.viz_metrics.territories(metrics)
