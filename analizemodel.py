import matplotlib
matplotlib.use('Qt5Agg')

import matplotlib.pyplot as plt
import netCDF4 as nc
from netCDF4 import num2date
import numpy as np
import os

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

# Plotting the data
plt.figure(figsize=(10, 5))
plt.plot(time_dates_np, wap_time_series)
plt.title('Vertical Velocity (wap) Over Time at Specific Location')
plt.xlabel('Time')
plt.ylabel('Vertical Velocity (wap)')
plt.grid()

# Save the figure to a specific folder
output_folder = './output'  # Specify your output folder here
os.makedirs(output_folder, exist_ok=True)  # Create folder if it doesn't exist

# Save the figure as a PNG file (you can change the format by changing the extension)
output_file_path = os.path.join(output_folder, 'vertical_velocity_plot.png')
plt.savefig(output_file_path, bbox_inches='tight')  # Save with tight layout

# Optionally show the plot (if desired)
plt.show()
