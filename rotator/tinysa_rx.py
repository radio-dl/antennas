from tinyscpi import tinySCPI
import time

#print(tinySCPI.user_input("*IDN?"))

freq_hz = int(2200e6) 
#tinySCPI.user_input(f"FREQ:START {freq_hz}")
#tinySCPI.user_input(f"FREQ:STOP {freq_hz}")
# Give the instrument time to perform the measurement
time.sleep(2)
# Query the scan measurement data
response = tinySCPI.user_input(f"FREQ:SCAN:MEAS {freq_hz} {freq_hz}")
#print("response length:", len(response))
lines = response.strip().splitlines()
# Extract the first line
last_line = lines[-1] if lines else None
dbm_str = last_line.split()[0]  # get first column
dbm_value = float(dbm_str)
print("dBm reading:", dbm_value)

# Parse the first dBm value
#if first_line:
#    dbm_str = first_line.split()[0]  # get first column
#    dbm_value = float(dbm_str)
#    print("First dBm reading:", dbm_value)
#else:
#    print("No data received")
