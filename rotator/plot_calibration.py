import json
import matplotlib.pyplot as plt
import numpy as np
import os

CALIBRATION_FILE = "calibration.json"

def load_calibration():
    if not os.path.exists(CALIBRATION_FILE):
        print(f"File {CALIBRATION_FILE} not found.")
        return {}
    with open(CALIBRATION_FILE, "r") as f:
        return json.load(f)

def plot_polar(calibration_data):
    angles_deg = sorted(int(k) for k in calibration_data)
    angles_rad = [np.deg2rad(a) for a in angles_deg]
    db_values = [calibration_data[str(a)] for a in angles_deg]
    # Normalize so maximum dB value becomes 0
    max_db = max(db_values)
    db_values = [v - max_db for v in db_values]


    # Close the loop for polar plot (optional)
    if angles_deg[0] != 0 or angles_deg[-1] != 360:
        angles_rad.append(angles_rad[0])
        db_values.append(db_values[0])

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    #ax.plot(angles_rad, db_values, marker='o')
    ax.plot(angles_rad, db_values)
    ax.set_theta_zero_location('N')  # 0° at top
    ax.set_theta_direction(-1)       # Clockwise
    ax.set_title("Calibration Polar Plot (dB vs Angle)", va='bottom')
    ax.set_rlabel_position(135)      # Move radial labels

    # Convert dB to linear
    linear = np.array([10**(v / 10) for v in db_values])

    # Approximate integration over full circle
    delta_theta = 2 * np.pi / len(linear)  # step size in radians
    total_power = np.sum(linear * delta_theta)

    # Directivity in linear and dB
    directivity = 1 / (total_power / (2 * np.pi))
    directivity_db = 10 * np.log10(directivity)

    print(f"Estimated Directivity: {directivity:.2f} (linear), {directivity_db:.2f} dB")

    plt.show()



def main():
    calibration_data = load_calibration()
    if calibration_data:
        plot_polar(calibration_data)

if __name__ == "__main__":
    main()
