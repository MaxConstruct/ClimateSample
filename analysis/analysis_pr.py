# %%
import xarray as xr
from analysis import netcdf_util as ut
import numpy as np
import pandas as pd
from setting import dataset_path, csv_path

# %%
pr_ds = xr.load_dataarray(dataset_path / r'cru_sea_pr_monthly_1981-2019.nc')
# %%
decade_range = np.stack(np.array([[1981, 1991, 2001, 2011], [1990, 2000, 2010, 2019]]), axis=1)
decades_data = [ut.select_year(pr_ds, *i) for i in decade_range]
decades_mean_monthly = [
    da.groupby('time.month').mean(dim='time').mean(dim=['lat', 'lon'])
    for da in decades_data
]
df_monthly = pd.DataFrame({'Month': np.arange(1, 13, 1)}).set_index('Month')
for i, da in enumerate(decades_mean_monthly):
    df_monthly['-'.join(decade_range[i].astype(str))] = da.values
df_monthly['Mean'] = df_monthly.mean(axis=1)


# %%
dat = {
    'Year': [],
    'Month 5-10': [],
    'Month 11-4': []
}
for year in range(1981, 2020):
    y = pr_ds.where(pr_ds.time.dt.year == year, drop=True)
    month_5_10 = y.where((y.time.dt.month >= 5) & (y.time.dt.month <= 10), drop=True).sum(dim='time', skipna=False)
    month_11_4 = y.where(~((y.time.dt.month >= 5) & (y.time.dt.month <= 10)), drop=True).sum(dim='time', skipna=False)
    dat['Year'].append(year)
    dat['Month 5-10'].append(month_5_10.mean().values)
    dat['Month 11-4'].append(month_11_4.mean().values)
swmr_nemr_39_year = pd.DataFrame(dat).set_index('Year')


# %%
pr_39_year = pr_ds.resample(time='AS').sum(skipna=False).mean(dim='time')
dat = []
len_lat, len_lon = pr_39_year.shape
for lat in pr_39_year.lat.values:
    t = pr_39_year.sel(lat=lat)
    dat.append(pd.DataFrame({
        'latitude': np.array([lat] * len_lon),
        'longitude': t.lon.values,
        'Pmean': t.values
    }))
new_format = pd.concat(dat)
#%%
df_monthly.to_excel(csv_path / 'Analysis_pr_39_year_monthly.xlsx')
new_format.dropna().to_excel(csv_path / 'Analysis_pr_loc_mean_annual.xlsx')
swmr_nemr_39_year.to_excel(csv_path / 'Analysis_pr_swmr_nemr_39_year.xlsx')
#%%
df_monthly.to_csv(csv_path / 'csv' / 'Analysis_pr_39_year_monthly.csv')
new_format.dropna().to_csv(csv_path / 'csv' / 'Analysis_pr_loc_mean_annual.csv')
swmr_nemr_39_year.to_csv(csv_path / 'csv' / 'Analysis_pr_swmr_nemr_39_year.csv')
#%%
df_monthly.to_csv(csv_path / 'csv' / 'Analysis_pr_39_year_monthly.tsv', sep='\t')
new_format.dropna().to_csv(csv_path / 'csv' / 'Analysis_pr_loc_mean_annual.tsv', sep='\t')
swmr_nemr_39_year.to_csv(csv_path / 'csv' / 'Analysis_pr_swmr_nemr_39_year.tsv', sep='\t')
