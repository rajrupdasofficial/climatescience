import matplotlib
matplotlib.use('Qt5Agg')

import matplotlib.pyplot as plt
import netCDF4 as nc
from netCDF4 import num2date
import numpy as np
import datetime
import matplotlib.dates as mdates

# Select a specific latitude and longitude index
lat_index = 32
lon_index = 64

# Load the dataset
dataset = nc.Dataset('./dataset/nasa_data1.nc')

# Extract 'wap' data
wap_data = dataset.variables['wap'][:]

# Extract wap data for that location over time
wap_time_series = wap_data[:, :, lat_index, lon_index]

# Accessing time variable
time_data = dataset.variables['time'][:]
time_units = dataset.variables['time'].units

# Convert time data to datetime objects
time_dates = num2date(time_data, units=time_units)

# Convert cftime objects to numpy datetime64 for compatibility with matplotlib
time_dates_np = np.array(time_dates).astype('datetime64[s]')

# Define date range for 2024-2026
start_date = datetime.datetime(2024, 1, 1)
end_date = datetime.datetime(2026, 12, 31)

# Convert datetime to matplotlib date numbers
start_num = mdates.date2num(start_date)
end_num = mdates.date2num(end_date)

# Create mask for specified date range
mask_range = (mdates.date2num(time_dates_np) >= start_num) & (mdates.date2num(time_dates_np) <= end_num)

# Extract vertical velocity data for the range
wap_range = wap_time_series[mask_range]
time_range = time_dates_np[mask_range]

# Calculate statistics
mean_wap = np.mean(wap_range)
min_wap = np.min(wap_range)
max_wap = np.max(wap_range)
std_wap = np.std(wap_range)

# Print statistics
print("Vertical Velocity (WAP) Statistics (2024-2026):")
print(f"Mean Vertical Velocity: {mean_wap:.4f}")
print(f"Minimum Vertical Velocity: {min_wap:.4f}")
print(f"Maximum Vertical Velocity: {max_wap:.4f}")
print(f"Standard Deviation: {std_wap:.4f}")

# Plotting the data
plt.figure(figsize=(20, 10))
plt.plot(time_range, wap_range, label='Vertical Velocity')
plt.title('Vertical Velocity (WAP) from 2024 to 2026')
plt.xlabel('Time')
plt.ylabel('Vertical Velocity')
plt.grid(True)

# Format x-axis
plt.gcf().autofmt_xdate()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

# Add horizontal line for mean
plt.axhline(y=mean_wap, color='r', linestyle='--',
            label=f'Mean Vertical Velocity: {mean_wap:.4f}')

plt.legend()
plt.tight_layout()
plt.show()
