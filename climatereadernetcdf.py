import netCDF4 as nc
from netCDF4 import num2date
#open the dataset using netcdf
dataset = nc.Dataset('./dataset/nasa_data1.nc')

#accessing wap dataset
wap_data = dataset.variables['wap'][:]
#print(wap_data)

# Accessing latitude and longitude
latitudes = dataset.variables['lat'][:]
longitudes = dataset.variables['lon'][:]

#print("Latitudes:", latitudes)
#print("Longitudes:", longitudes)

# Accessing time variable
time_data = dataset.variables['time'][:]
time_units = dataset.variables['time'].units
#print("Time Units:", time_units)

# Convert time data to datetime objects
time_dates = num2date(time_data, units=time_units)
print("Time Dates:", time_dates)
