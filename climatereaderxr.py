# import netCDF4 as nc
# import numpy as np
import xarray as xr
# Open the NetCDF file
# dataset = nc.Dataset('./dataset/nasa_data1.nc')

# # Print dataset information
# print(dataset)

ds = xr.open_dataset('./dataset/nasa_data1.nc')

# Inspect the dataset
print(ds)
