import matplotlib
matplotlib.use('Qt5Agg')
import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import num2date
import matplotlib.dates as mdates

# Open the NetCDF dataset
datasets = nc.Dataset('./dataset/nasa-data3.nc')

# Extract the heat flux variable
hfss_col = datasets.variables['hfss']

# Get dimensions
time_dim = datasets.variables['time']
lat_dim = datasets.variables['lat']
lon_dim = datasets.variables['lon']

# Extract data
hfss_data = hfss_col[:]  # This retrieves the entire 3D array

# Convert time to matplotlib-compatible dates
time_values = num2date(time_dim[:], time_dim.units)
time_numbers = mdates.date2num(time_values)

# Data shape: (time, lat, lon)
print("Data shape:", hfss_data.shape)

# Example: Get mean heat flux across all latitudes and longitudes for each time step
mean_hfss_over_time = np.mean(hfss_data, axis=(1, 2))

# Visualization example
plt.figure(figsize=(15, 6))
plt.plot(time_numbers, mean_hfss_over_time)
plt.title('Mean Surface Upward Sensible Heat Flux Over Time')
plt.xlabel('Time')
plt.ylabel('Heat Flux (W m-2)')

# Format x-axis to show dates nicely
plt.gcf().autofmt_xdate()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

plt.tight_layout()
plt.show()
