# Load data from file
import numpy as np

with open("output.txt") as f:
    db_values = np.array([float(line.strip()) for line in f if line.strip()])
print("Max:", np.max(db_values))
print("Min:", np.min(db_values))
normalized_values = [v - max(db_values) for v in db_values]


angles_deg = np.arange(0, 360, 6)  # 60 points from 0 to 354
angles_rad = np.radians(angles_deg)
radii = np.array(normalized_values)

# Convert from dB to linear scale
lin_values = 10 ** (db_values / 10)
# Find max value
u_max = np.max(lin_values)
# Integrate over 360° (every 6° = 60 samples)
phi = np.linspace(0, 2 * np.pi, len(lin_values), endpoint=False)
dphi = 2 * np.pi / len(lin_values)
# Approximate integral using trapezoidal rule
avg_u = np.sum(lin_values) * dphi / (2 * np.pi)
# Directivity (linear)
D = u_max / avg_u
# Convert to dB
D_dB = 10 * np.log10(D)

print(f"Estimated Directivity: {D:.2f} (linear), {D_dB:.2f} dBi")

import matplotlib.pyplot as plt

plt.figure(figsize=(6,6))
ax = plt.subplot(111, polar=True)

ax.plot(angles_rad, radii, marker='o', linestyle='-')
ax.set_theta_direction(-1)  # optional: clockwise
ax.set_theta_zero_location('N')  # optional: 0° at the top

plt.title("Polar Plot of 60 Measurements")
plt.tight_layout()
plt.show()
