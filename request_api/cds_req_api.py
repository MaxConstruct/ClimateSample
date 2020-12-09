#%%
"""
----
JIRAWAT NAFUNG
----

ERA5 Reanalysis Dataset.
ERA5 provides hourly estimates of a large number of atmospheric, land and oceanic climate variables.
Code below demonstrate how to retrieve dataset as netCDF format file

Visit ECMWF site for more detail about ERA5:
https://confluence.ecmwf.int/display/CKB/ERA5%3A+data+documentation

More detail about CDS API:
https://confluence.ecmwf.int/display/CKB/How+to+download+ERA5

More detail about netCDF:
https://www.unidata.ucar.edu/software/netcdf/
"""

import cdsapi
import os
from setting import dataset_path
# API key for retrieving data.

KEY = 'xxxxx:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
# API Config
path = os.path.join(os.environ.get('USERPROFILE'), '.cdsapirc')
if not os.path.exists(path):
    print('Config file not found. Creating new config file')
    with open(path, mode='w') as config:
        s = f"""
        url: https://cds.climate.copernicus.eu/api/v2
        key: {KEY}
        """
        config.write(s.strip())
else:
    print('Config file is found.')

# Downloading dataset in netCDF format.
c = cdsapi.Client()
#%%

c.retrieve(
    'reanalysis-era5-land-monthly-means',
    {
        'format': 'netcdf',
        'product_type': 'monthly_averaged_reanalysis_by_hour_of_day',
        'variable': '2m_temperature',
        'year': [
            '1981', '1982', '1983',
            '1984', '1985', '1986',
            '1987', '1988', '1989',
            '1990', '1991', '1992',
            '1993', '1994', '1995',
            '1996', '1997', '1998',
            '1999', '2000', '2001',
            '2002', '2003', '2004',
            '2005', '2006', '2007',
            '2008', '2009', '2010',
            '2011', '2012', '2013',
            '2014', '2015', '2016',
            '2017', '2018', '2019',
        ],
        'month': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
        ],
        'time': '00:00',
        'area': [
            24.5, 92.5, -12.5,
            142.5,
        ],
    },
    dataset_path / 'era5_sea_tmean_monthly_1981-2019.nc')


