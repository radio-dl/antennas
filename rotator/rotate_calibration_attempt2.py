import serial
import serial.tools.list_ports
import json
import os
import time
from tinyscpi import tinySCPI

CALIBRATION_FILE = "calibration_new.json"
FREQ_HZ = int(2400e6)
STEP_ANGLE = 6
DELAY_AFTER_ROTATE = 2.5  # Adjust depending on your motor speed

# Give USB device time to fully initialize
print("Waiting for tinySA...")
time.sleep(3)

try:
    idn = tinySCPI.user_input("*IDN?")
    print("tinySA connected:", idn)
except Exception as e:
    print("Failed to connect to tinySA:", e)
    exit(1)

def get_measurement():
    try:
        time.sleep(2)
        response = tinySCPI.user_input(f"FREQ:SCAN:MEAS {FREQ_HZ} {FREQ_HZ}")
        #print("Full response:\n", response)
        lines = response.strip().splitlines()
        last_line = lines[-1] if lines else None
        dbm_str = last_line.split()[0]  # first column is dBm
        dbm_value = float(dbm_str)
        print(f"dBm reading: {dbm_value}")
        return dbm_value
    except Exception as e:
        print(f"Measurement failed: {e}")
        return None

import serial
def rotate():
    with serial.Serial("COM4", 9600, timeout=1) as ser:
        time.sleep(2)
        value=int(6)
        ser.write(f"{value}".encode())
        
success=get_measurement()
print(success)
rotate()
print("done rotation")

db_list=[]
for x in range(0, 360, 6):
    print("angle:", x)
    success=get_measurement()
    db_list.append(success)
    data = {"angle": x, "value": success}
    with open("readings.jsonl", "a") as f:
        f.write(json.dumps(data) + "\n")
    rotate()

print("done loop")
print(db_list)

with open('output.txt', 'w') as f:
    for item in db_list:
        f.write(f"{item}\n")