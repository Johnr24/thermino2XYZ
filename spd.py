import numpy as np
import colour
from colour import SpectralDistribution, sd_to_XYZ, XYZ_to_xy

# Read the spectral data from the file
file_path = 'laser.txt'
data = np.loadtxt(file_path, skiprows=1)

# Extract wavelengths and values
wavelengths = data[:, 0]
values = data[:, 1] / 100.0  # Convert percentage to decimal

# Initialize variables to store the current interval and its values
current_nm = int(wavelengths[0])
interval_values = []
mean_values = []

# Iterate through the data
for wavelength, value in zip(wavelengths, values):
    nm = int(wavelength)
    if nm == current_nm:
        interval_values.append(value)
    else:
        # Compute the mean for the current interval
        mean_value = np.mean(interval_values)
        mean_values.append((current_nm, mean_value))
        
        # Reset for the next interval
        current_nm = nm
        interval_values = [value]

# Don't forget to add the last interval
if interval_values:
    mean_value = np.mean(interval_values)
    mean_values.append((current_nm, mean_value))

# Separate the mean values into wavelengths and values
mean_wavelengths, mean_values = zip(*mean_values)

# Create a SpectralDistribution object with the mean values
sd = SpectralDistribution(mean_values, mean_wavelengths)

# Convert the spectral distribution to XYZ coordinates
XYZ = sd_to_XYZ(sd)

# Convert XYZ coordinates to xy chromaticity coordinates
xy = XYZ_to_xy(XYZ)

print("XYZ tristimulus values:", XYZ)
print("White point (xy chromaticity coordinates):", xy)