import serial
import serial.tools.list_ports
import json
import os
import time
from tinyscpi import tinySCPI

CALIBRATION_FILE = "calibration.json"
FREQ_HZ = int(700e6)
STEP_ANGLE = 6
DELAY_AFTER_ROTATE = 2.5  # Adjust depending on your motor speed
time.sleep(2)

import time
from tinyscpi import tinySCPI

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
        print("Full response:\n", response)
        lines = response.strip().splitlines()
        last_line = lines[-1] if lines else None
        dbm_str = last_line.split()[0]  # first column is dBm
        print("dbm string:", dbm_str)
        dbm_value = float(dbm_str)
        print(f"dBm reading: {dbm_value}")
        return dbm_value
    except Exception as e:
        print(f"Measurement failed: {e}")
        return None

def find_arduino_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "Arduino" in port.description or "USB Serial" in port.description:
            return port.device
    return None

def load_calibration():
    if os.path.exists(CALIBRATION_FILE):
        with open(CALIBRATION_FILE, "r") as f:
            return json.load(f)
    return {}

def save_calibration(data):
    with open(CALIBRATION_FILE, "w") as f:
        json.dump(data, f, indent=2)

def main():

    get_measurement()
    
    port = find_arduino_port()
    if not port:
        print("Arduino not found.")
        return

    print(f"Found Arduino on {port}")
    calibration_data = load_calibration()

    with serial.Serial(port, 9600, timeout=2) as ser:
        time.sleep(3)  # Wait for Arduino to reset
        for angle in range(0, 360, STEP_ANGLE):
            print(f"\n--- Moving to {angle} degrees ---")
            
            # Send angle command to Arduino
            ser.write(b"6")
            time.sleep(DELAY_AFTER_ROTATE)

            db_value = get_measurement()
            if db_value is not None:
                calibration_data[str(angle)] = db_value
                save_calibration(calibration_data)
                print(f"Saved: {angle}° => {db_value} dB")
            else:
                print(f"Skipped saving for angle {angle} due to measurement error.")
            time.sleep(0.2)

if __name__ == "__main__":
    main()
