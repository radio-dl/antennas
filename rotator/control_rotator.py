import serial
import serial.tools.list_ports

def find_arduino_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "Arduino" in port.description or "USB Serial" in port.description:
            return port.device
    return None

def main():
    port = find_arduino_port()
    if not port:
        print("Arduino not found. Please check the connection.")
        return

    print(f"Found Arduino on {port}")

    position = 0  # Accumulated position

    try:
        with serial.Serial(port, 115200, timeout=1) as ser:
            while True:
                user_input = input("Enter +x or -x: ").strip()
                #if user_input not in ["6", "-6"]:
                #    print("Only +6 or -6 are allowed.")
                #    continue
                value = int(user_input)
                position += value  # Update accumulated position

                ser.write(f"{value}".encode())
                print(f"Sent {value} to Arduino | Current position: {position}")
    except serial.SerialException as e:
        print(f"Failed to open serial port: {e}")

if __name__ == "__main__":
    main()
