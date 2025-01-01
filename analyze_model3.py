import matplotlib
matplotlib.use('Qt5Agg')
import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import num2date
import matplotlib.dates as mdates
import datetime

def calculate_temperature_rise(heat_flux_data):
    """
    Calculate estimated temperature rise from heat flux data

    Parameters:
    - heat_flux_data: Array of heat flux measurements

    Returns:
    - Estimated temperature rise in °C
    """
    # Thermodynamic constants
    specific_heat_capacity = 1005  # J/kg*K (for air)
    air_density = 1.225  # kg/m³
    time_duration = len(heat_flux_data)  # Assuming daily measurements

    # Calculate cumulative heat energy
    total_heat_energy = np.sum(heat_flux_data)

    # Estimate temperature rise
    temperature_rise = (total_heat_energy /
                        (specific_heat_capacity *
                         air_density *
                         time_duration))

    return temperature_rise

# Open the NetCDF dataset
datasets = nc.Dataset('./dataset/nasa_data3.nc')

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

# Calculate mean heat flux across all latitudes and longitudes for each time step
mean_hfss_over_time = np.mean(hfss_data, axis=(1, 2))

# Define date range for 2024-2026
start_date = datetime.datetime(2024, 1, 1)
end_date = datetime.datetime(2026, 12, 31)

# Convert datetime to matplotlib date numbers
start_num = mdates.date2num(start_date)
end_num = mdates.date2num(end_date)

# Create mask for specified date range
mask_range = (time_numbers >= start_num) & (time_numbers <= end_num)

# Extract heat flux data for the range
heat_flux_range = mean_hfss_over_time[mask_range]
time_range = time_numbers[mask_range]

# Calculate comprehensive heat flux statistics
mean_heat_flux = np.mean(heat_flux_range)
min_heat_flux = np.min(heat_flux_range)
max_heat_flux = np.max(heat_flux_range)
std_heat_flux = np.std(heat_flux_range)
total_heat_rise = np.sum(heat_flux_range)

# Calculate estimated temperature rise
estimated_temp_rise = calculate_temperature_rise(heat_flux_range)

# Print detailed statistics
print("Heat Flux Statistics (2024-2026):")
print(f"Mean Heat Flux: {mean_heat_flux:.2f} W m-2")
print(f"Minimum Heat Flux: {min_heat_flux:.2f} W m-2")
print(f"Maximum Heat Flux: {max_heat_flux:.2f} W m-2")
print(f"Standard Deviation: {std_heat_flux:.2f} W m-2")
print(f"Total Heat Rise: {total_heat_rise:.2f} W m-2")
print(f"Estimated Temperature Rise: {estimated_temp_rise:.2f}°C")

# Enhanced Visualization
plt.figure(figsize=(20,10))

# Heat Flux Plot
plt.subplot(2, 1, 1)
plt.plot(time_range, heat_flux_range, label='Heat Flux', color='red')
plt.title('Surface Upward Sensible Heat Flux (2024-2026)', fontsize=15)
plt.xlabel('Time', fontsize=12)
plt.ylabel('Heat Flux (W m-2)', fontsize=12)
plt.gcf().autofmt_xdate()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.grid(True, linestyle='--', alpha=0.7)
plt.axhline(y=mean_heat_flux, color='green', linestyle='--',
            label=f'Mean Heat Flux: {mean_heat_flux:.2f} W m-2')
plt.legend()

# Temperature Rise Plot
plt.subplot(2, 1, 2)
plt.plot(time_range, np.cumsum(heat_flux_range), label='Cumulative Heat Rise', color='blue')
plt.title('Cumulative Heat Rise (2024-2026)', fontsize=15)
plt.xlabel('Time', fontsize=12)
plt.ylabel('Cumulative Heat Rise', fontsize=12)
plt.gcf().autofmt_xdate()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

plt.tight_layout()
plt.show()
