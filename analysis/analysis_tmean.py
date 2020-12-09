# %%
import xarray as xr
from analysis import netcdf_util as ut
import numpy as np
import pandas as pd
from setting import dataset_path, csv_path

# %%
tmean_ds = xr.load_dataarray(dataset_path / 'era5_sea_tmean_monthly_1981-2019.nc').rename(
    {'latitude': 'lat', 'longitude': 'lon'})
tmean_ds = tmean_ds - 273.15
# %%
tmean_yearly = tmean_ds.resample(time='AS').mean(skipna=False)
tmean_line_39_year = tmean_yearly.mean(dim=['lat', 'lon']).to_dataframe('Tmean')
tmean_line_39_year.index = tmean_line_39_year.index.strftime('%Y')
tmean_mean_39_year = tmean_yearly.mean(dim='time')
# %%
pr = xr.load_dataarray(dataset_path / 'cru_sea_pr_monthly_1981-2019.nc')
downscale_tmean = tmean_mean_39_year.interp(lat=pr.lat, lon=pr.lon)
# %%
dat = []
len_lat, len_lon = downscale_tmean.shape
for lat in downscale_tmean.lat.values:
    t = downscale_tmean.sel(lat=lat)
    dat.append(pd.DataFrame({
        'latitude': np.array([lat] * len_lon),
        'longitude': t.lon.values,
        'Tmean': t.values
    }))
new_format = pd.concat(dat)

# %%
decade_range = np.stack(np.array([[1981, 1991, 2001, 2011], [1990, 2000, 2010, 2019]]), axis=1)
decades_data = [ut.select_year(tmean_ds, *i) for i in decade_range]
decades_mean_monthly = [
    da.groupby('time.month').mean(dim='time').mean(dim=['lat', 'lon'])
    for da in decades_data
]
df_monthly = pd.DataFrame({'Month': np.arange(1, 13, 1)}).set_index('Month')
for i, da in enumerate(decades_mean_monthly):
    df_monthly['-'.join(decade_range[i].astype(str))] = da.values
df_monthly['Mean'] = df_monthly.mean(axis=1)

# %%
df_monthly.to_excel(csv_path / 'Analysis_tmean_39_year_monthly.xlsx')
tmean_line_39_year.to_excel(csv_path / 'Analysis_tmean_39_year.xlsx')
new_format.dropna().to_excel(csv_path / 'Analysis_tmean_loc_mean_annual.xlsx')
# %%
df_monthly.to_csv(csv_path / 'csv' / 'Analysis_tmean_39_year_monthly.csv')
tmean_line_39_year.to_csv(csv_path / 'csv' / 'Analysis_tmean_39_year.csv')
new_format.dropna().to_csv(csv_path / 'csv' / 'Analysis_tmean_loc_mean_annual.csv')
# %%
df_monthly.to_csv(csv_path / 'csv'/'Analysis_tmean_39_year_monthly.tsv', sep='\t')
tmean_line_39_year.to_csv(csv_path / 'csv'/'Analysis_tmean_39_year.tsv', sep='\t')
new_format.dropna().to_csv(csv_path / 'csv'/'Analysis_tmean_loc_mean_annual.tsv', sep='\t')
