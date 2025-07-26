import json
import os
import numpy as np
import matplotlib.pyplot as plt
import math

CALIBRATION_FILE = "calibration.json"
#coil monopole at 700 MHz, typical monopole has gain of 3.7 dBi
# === User Settings ===
S11_dB = -15         # Measured S11 in dB
eta_rad = 0.80        # Estimated radiation efficiency (0–1)

def load_calibration():
    if not os.path.exists(CALIBRATION_FILE):
        raise FileNotFoundError(f"Calibration file '{CALIBRATION_FILE}' not found.")
    with open(CALIBRATION_FILE, "r") as f:
        return json.load(f)

def normalize_db_values(db_values):
    max_db = max(db_values)
    return [v - max_db for v in db_values]

def estimate_directivity(normalized_db_values):
    linear = np.array([10**(v / 10) for v in normalized_db_values])
    delta_theta = 2 * np.pi / len(linear)
    total_power = np.sum(linear * delta_theta)
    directivity_linear = 1 / (total_power / (2 * np.pi))
    directivity_db = 10 * np.log10(directivity_linear)
    return directivity_db

def estimate_gain(D_dB, S11_dB, eta_rad):
    gamma = 10 ** (S11_dB / 20)
    mismatch_eff = 1 - gamma ** 2
    total_eff = eta_rad * mismatch_eff
    G_dB = D_dB + 10 * math.log10(total_eff)
    return G_dB, mismatch_eff, total_eff

def plot_polar(angles_deg, db_values):
    angles_rad = [np.deg2rad(a) for a in angles_deg]
    norm = (np.array(db_values) - min(db_values)) / (max(db_values) - min(db_values))
    cmap = plt.colormaps['coolwarm']
    colors = [cmap(n) for n in norm]

    # Close loop if needed
    if angles_deg[0] != 0 or angles_deg[-1] != 360:
        angles_rad.append(angles_rad[0])
        db_values.append(db_values[0])
        colors.append(colors[0])

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_title("Antenna Pattern (Normalized dB)", va='bottom')
    ax.set_rlabel_position(135)

    # Plot colored lines between points
    for i in range(len(angles_rad)-1):
        xs = [angles_rad[i], angles_rad[i+1]]
        ys = [db_values[i], db_values[i+1]]
        avg_norm = (norm[i] + norm[(i+1) % len(norm)]) / 2
        ax.plot(xs, ys, color=cmap(avg_norm), linewidth=2)

    # Annotate max point
    max_idx = np.argmax(db_values)
    ax.annotate("0 dB (max)", 
                xy=(angles_rad[max_idx], db_values[max_idx]),
                xytext=(10, 10),
                textcoords='offset points',
                ha='left', va='bottom',
                fontsize=9,
                color='red',
                arrowprops=dict(arrowstyle="->", color='red'))

    plt.show()

def main():
    # Load data
    calibration_data = load_calibration()
    angles_deg = sorted(int(k) for k in calibration_data)
    raw_db_values = [calibration_data[str(k)] for k in angles_deg]

    # Normalize and estimate
    normalized_db = normalize_db_values(raw_db_values)
    D_dB = estimate_directivity(normalized_db)
    G_dB, mismatch_eff, total_eff = estimate_gain(D_dB, S11_dB, eta_rad)

    # Print summary
    print(f"\n--- ANTENNA PERFORMANCE SUMMARY ---")
    print(f"Estimated Directivity (D):      {D_dB:.2f} dB")
    print(f"S11 (return loss):             {S11_dB} dB")
    print(f"Reflection efficiency:         {mismatch_eff*100:.1f} %")
    print(f"Radiation efficiency:          {eta_rad*100:.1f} %")
    print(f"Total efficiency (η_total):    {total_eff*100:.1f} %")
    print(f"Estimated Gain (G):            {G_dB:.2f} dB\n")

    # Plot
    plot_polar(angles_deg, normalized_db)

if __name__ == "__main__":
    main()
