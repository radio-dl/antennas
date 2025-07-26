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
    # Parse and sort angle -> dB
    angles_deg = sorted(int(k) for k in calibration_data)
    angles_rad = [np.deg2rad(a) for a in angles_deg]
    db_values = [calibration_data[str(a)] for a in angles_deg]
    # Normalize so maximum dB value becomes 0
    max_db = max(db_values)
    db_values = [v - max_db for v in db_values]

    # Normalize dB values for color mapping (lower = blue, higher = red)
    db_array = np.array(db_values)
    norm = (db_array - db_array.min()) / (db_array.max() - db_array.min())

    cmap = plt.cm.get_cmap('coolwarm')
    colors = [cmap(n) for n in norm]

    # Close the loop if not full circle
    if angles_deg[0] != 0 or angles_deg[-1] != 360:
        angles_rad.append(angles_rad[0])
        db_values.append(db_values[0])
        colors.append(colors[0])

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_title("Directivity Polar Plot (dB vs Angle)", va='bottom')
    ax.set_rlabel_position(135)

    # Plot colored line segments between points
    for i in range(len(angles_rad)-1):
        xs = [angles_rad[i], angles_rad[i+1]]
        ys = [db_values[i], db_values[i+1]]
        # Color line segment by average of the two points
        avg_norm = (norm[i] + norm[(i+1) % len(norm)]) / 2
        ax.plot(xs, ys, color=cmap(avg_norm), linewidth=2)

    # Plot points with edge colors
    #ax.scatter(angles_rad, db_values, c=colors, cmap='coolwarm', s=1, edgecolors='k', zorder=5)

    # Convert dB to linear
    linear = np.array([10**(v / 10) for v in db_values])

    # Approximate integration over full circle
    delta_theta = 2 * np.pi / len(linear)  # step size in radians
    total_power = np.sum(linear * delta_theta)

    # Directivity in linear and dB
    directivity = 1 / (total_power / (2 * np.pi))
    directivity_db = 10 * np.log10(directivity)

    print(f"Estimated Directivity: {directivity:.2f} (linear), {directivity_db:.2f} dB")

    import math

    #D_dB = 6.5  # estimated directivity from pattern (in dB)
    S11_dB = -18
    eta_rad = 0.50 #estimated radiation efficiency (50%)
    Gamma = 10 ** (S11_dB / 20)
    mismatch_eff = 1 - Gamma ** 2
    total_eff = eta_rad * mismatch_eff
    G_dB = directivity_db + 10 * math.log10(total_eff)

    print(f"Estimated Gain ≈ {G_dB:.2f} dB")

    # Annotate max dB point
    max_index = np.argmax(db_array)
    max_angle = angles_rad[max_index]
    max_db = db_array[max_index]
    ax.annotate(f"{max_db:.1f} dB",
                xy=(max_angle, max_db),
                xytext=(10, 10),
                textcoords='offset points',
                ha='left', va='bottom',
                fontsize=10, color='red',
                arrowprops=dict(arrowstyle="->", color='red'))

    plt.show()

def main():
    calibration_data = load_calibration()
    if calibration_data:
        plot_polar(calibration_data)

if __name__ == "__main__":
    main()
