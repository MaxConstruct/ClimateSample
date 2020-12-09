#%%
# For more detail about CRU dataset:
# https://catalogue.ceda.ac.uk/uuid/89e1e34ec3554dc98594a5732622bce9

from pathlib import Path
from setting import dataset_path
import numpy as np
import ftplib
from analysis import netcdf_util as ut

#%%
decade_range = np.stack(np.array([[1981, 1991, 2001, 2011], [1990, 2000, 2010, 2019]]), axis=1)
links = [
    Path(f'/badc/cru/data/cru_ts/cru_ts_4.04/data/pre/cru_ts4.04.{i[0]}.{i[1]}.pre.dat.nc.gz')
    for i in decade_range
]

#%%

auth = 'Username', 'Password'
f = ftplib.FTP('ftp.ceda.ac.uk', *auth)
#%%
for link in links:
    with open(dataset_path / link.name, "wb") as file:
        f.retrbinary(f'RETR {link.as_posix()}', file.write)

#%%
import xarray as xr
zipfiles = sorted(dataset_path.glob('*.gz'))
mf_ds = [
    xr.open_dataset(i).rename({'pre': 'pr'}).pr
    for i in zipfiles
]
new_ds = xr.concat(mf_ds, dim='time')
crop_ds = ut.crop_dataset_from_bound(new_ds, lon_bound=[92.5, 142.5], lat_bound=[-12.5, 24.5])
#%%
crop_ds.to_netcdf(dataset_path / 'cru_sea_pr_monthly_1981-2019.nc')
