from tinyscpi import tinySCPI
import time

freq_hz = int(2200e6)

# Wait for the instrument to complete setup
time.sleep(2)

# Perform scan (single-frequency scan)
response = tinySCPI.user_input(f"FREQ:SCAN:MEAS {freq_hz} {freq_hz}")

# Parse lines and convert to float dBm values
lines = response.strip().splitlines()

# Extract valid dBm values
dbm_values = []
for line in lines:
    parts = line.strip().split()
    if parts:
        try:
            dbm = float(parts[0])  # assume first column is dBm
            dbm_values.append(dbm)
        except ValueError:
            pass  # skip lines that don't start with a float

# Compute and print mean
if dbm_values:
    print("Number of values:", len(dbm_values))
    avg_dbm = sum(dbm_values) / len(dbm_values)
    print(f"Average dBm: {avg_dbm:.2f}")
else:
    print("No valid dBm values found.")
