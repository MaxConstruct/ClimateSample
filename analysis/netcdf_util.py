# Import libraries and set configuration

# os used for path and directory management
import os

# xarray, is the most important library, used for manipulate netCDF Dataset operation
from pathlib import Path

import xarray as xr
import numpy as np

# matplotlib for plotting Dataset. cartopy for various map projection
from distributed.deploy.old_ssh import bcolors
from matplotlib.axes import Axes
from cartopy.mpl.geoaxes import GeoAxes
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature


# matplotlib setting
GeoAxes._pcolormesh_patched = Axes.pcolormesh

# %%
# Get country border for matplotlib
country_borders = cfeature.NaturalEarthFeature(
    category='cultural',
    name='admin_0_boundary_lines_land',
    scale='50m',
    facecolor='none')


# %%

def select_range(data, _min, _max):
    """
    create boolean array for selecting data within specific range.
    min <= data <= max
    :param data: DataArray to be selected.
    :param _min: min value
    :param _max: max value
    :return: boolean DataArray
    """
    return (data >= _min) & (data <= _max)


def crop_dataset_from_bound(data, lon_bound, lat_bound, x_name='lon', y_name='lat'):
    """
    Crop dataset in to specific lat & lon boundary
    :param data: xarray.Dataset to be cropped
    :param lon_bound: list that contain [min_lon, max_lon]
    :param lat_bound: list that contain [min_lat, max_lat]
    :return: cropped dataset as xarray.Dataset
    """

    mask_lon = select_range(data[x_name], lon_bound[0], lon_bound[1])
    mask_lat = select_range(data[y_name], lat_bound[0], lat_bound[1])

    return data.isel(lat=mask_lat, lon=mask_lon, drop=False)


def plot(data: xr.DataArray, time=None, savefig=None, show=True, set_global=False, country_border=True, **kwargs):
    """
    Quick plotting DataArray using PlateCarree as a projection
    Example: plot(dataset['tasmax'])

    :param data: DataArray to be plotted
    :param time: Specific time index to be plot using xarray.DataArray.isec method.
    Default is 0.
    :param savefig: path of figure to being save. Default is None (not save figure).
    :param show: Is showing graphic plot. Default is True.
    :param set_global: Set plotting to show global map.
    :param country_border: Is show country border on the plot. Default is True.
    :param kwargs: keyword arg pass to xarray.DataArray.plot
    :return: None
    """
    ax = plt.axes(projection=ccrs.PlateCarree())

    if time is None:
        if 'time' in data.coords and data.time.shape != ():
            data.isel(time=0).plot(ax=ax, **kwargs)
        else:
            data.plot(ax=ax, **kwargs)
    else:
        data.isel(time=time).plot(ax=ax, **kwargs)

    if country_border:
        ax.add_feature(country_borders, edgecolor='black')

    if set_global:
        ax.set_global()
    ax.coastlines()

    if savefig is not None:
        plt.savefig(savefig)

    if show:
        plt.show()
    plt.clf()
    plt.close()


def select_year(ds, from_y, to_y):
    return ds.sel(time=ds.time.dt.year.isin(np.arange(from_y, to_y + 1)))


def save_file(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


