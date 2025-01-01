import matplotlib
matplotlib.use('Qt5Agg')
import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import num2date
import matplotlib.dates as mdates
import datetime

# Load dataset
datasets = nc.Dataset('./dataset/nasa_data2.nc')

# Extract cloud cover data
clt_col = datasets.variables['clt']
ctl_exdata = clt_col[:]

# Convert time to matplotlib-compatible dates
time_dim = datasets.variables['time']
time_values = num2date(time_dim[:], time_dim.units)
time_numbers = mdates.date2num(time_values)

# Calculate cloud coverage percentage
tccp = np.mean(ctl_exdata, axis=(1,2))

# Define date range
start_date = datetime.datetime(2024, 1, 1)
end_date = datetime.datetime(2026, 12, 31)

# Convert datetime to matplotlib date numbers
start_num = mdates.date2num(start_date)
end_num = mdates.date2num(end_date)

# Create mask for specified date range
mask_range = (time_numbers >= start_num) & (time_numbers <= end_num)

# Extract cloud coverage data for the range
cloud_coverage_range = tccp[mask_range]
time_range = time_numbers[mask_range]

# Calculate comprehensive statistics
mean_coverage = np.mean(cloud_coverage_range)
min_coverage = np.min(cloud_coverage_range)
max_coverage = np.max(cloud_coverage_range)
std_coverage = np.std(cloud_coverage_range)

# Print detailed statistics
print("Cloud Coverage Statistics (2024-2026):")
print(f"Mean Cloud Coverage: {mean_coverage:.2f}%")
print(f"Minimum Cloud Coverage: {min_coverage:.2f}%")
print(f"Maximum Cloud Coverage: {max_coverage:.2f}%")
print(f"Standard Deviation: {std_coverage:.2f}%")

# Enhanced Visualization
plt.figure(figsize=(20,10))
plt.plot(time_range, cloud_coverage_range, label='Cloud Coverage')
plt.title('Cloud Coverage from 2024 to 2026', fontsize=15)
plt.xlabel('Time', fontsize=12)
plt.ylabel('Cloud Coverage (%)', fontsize=12)
plt.gcf().autofmt_xdate()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()
