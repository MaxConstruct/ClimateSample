import xarray as xr
from setting import dataset_path
from analysis import netcdf_util as ut
import numpy as np

#%%
temp_dataset = xr.open_dataarray(dataset_path / 'era5_sea_tmean_monthly_1981-2019.nc')
prec_dataset = xr.open_dataarray(dataset_path / 'cru_sea_pr_monthly_1981-2019.nc')

#%%
ut.plot(temp_dataset)
ut.plot(prec_dataset)
#%%
print('--Temperature')
print('\tDataset Shape: ', temp_dataset.shape)
print('\trecords: ', np.prod(temp_dataset.shape))
print()
print('--Precipitation')
print('\tDataset Shape: ', temp_dataset.shape)
print('\trecords: ', np.prod(temp_dataset.shape))
print()
print('Total Records:', np.prod(temp_dataset.shape) + np.prod(temp_dataset.shape))