# TODO: get more resolution stores
models = {
    'keisler': {
        '240x121': 'gs://weatherbench2/datasets/keisler/2020-240x121_equiangular_with_poles_conservative.zarr',
    },
    'pangu': {
        '240x121': 'gs://weatherbench2/datasets/pangu/2018-2022_0012_240x121_equiangular_with_poles_conservative.zarr',
    },
    'graphcast': {
        '240x121': 'gs://weatherbench2/datasets/graphcast/2020/date_range_2019-11-16_2021-02-01_12_hours-240x121_equiangular_with_poles_conservative.zarr',
    },
    'sphericalcnn': {
        '240x121': 'gs://weatherbench2/datasets/sphericalcnn/2020-240x121_equiangular_with_poles.zarr',
    },
    'fuxi': {
        '240x121': 'gs://weatherbench2/datasets/fuxi/2020-240x121_equiangular_with_poles_conservative.zarr',
    },
    'neuralgcm': {
        '240x121': 'gs://weatherbench2/datasets/neuralgcm_deterministic/2020-240x121_equiangular_with_poles_conservative.zarr',
    },
}

# TODO: get more resolution stores
era5 = {
    '240x121': 'gs://weatherbench2/datasets/era5/1959-2023_01_10-6h-240x121_equiangular_with_poles_conservative.zarr'
}
