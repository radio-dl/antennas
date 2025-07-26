import serial
import serial.tools.list_ports
import json
import os
import time

CALIBRATION_FILE = "calibration.json"

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
    port = find_arduino_port()
    if not port:
        print("Arduino not found.")
        return

    print(f"Found Arduino on {port}")
    calibration_data = load_calibration()
    current_angle = 0

    try:
        with serial.Serial(port, 9600, timeout=1) as ser:
            time.sleep(2)  # Wait for Arduino to reset after serial connect

            for angle in range(0, 360, 6):
                if str(angle) in calibration_data:
                    print(f"Skipping {angle}° (already calibrated)")
                    current_angle = angle
                    continue

                # Send +6 steps for every 6° movement after initial position
                steps_needed = (angle - current_angle) // 6
                for _ in range(steps_needed):
                    ser.write(b"6")
                    time.sleep(0.2)  # Small delay between steps

                current_angle = angle
                input("Press Enter when movement is complete...")

                while True:
                    try:
                        db_value = float(input(f"Enter dB value for angle {angle}: "))
                        break
                    except ValueError:
                        print("Invalid input. Enter a numeric value.")

                calibration_data[str(angle)] = db_value
                save_calibration(calibration_data)
                print(f"Saved: {angle}° => {db_value} dB")
                time.sleep(1)

    except serial.SerialException as e:
        print(f"Serial error: {e}")

if __name__ == "__main__":
    main()
