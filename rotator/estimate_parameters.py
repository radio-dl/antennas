import json
import numpy as np
import math
import os

CALIBRATION_FILE = "calibration.json"

def load_calibration():
    if not os.path.exists(CALIBRATION_FILE):
        raise FileNotFoundError(f"Calibration file '{CALIBRATION_FILE}' not found.")
    with open(CALIBRATION_FILE, "r") as f:
        return json.load(f)

def normalize_db_values(db_values):
    max_db = max(db_values)
    return [v - max_db for v in db_values]

def estimate_directivity(normalized_db_values):
    linear = np.array([10**(v / 10) for v in normalized_db_values])  # convert to linear
    delta_theta = 2 * np.pi / len(linear)                            # step in radians
    total_power = np.sum(linear * delta_theta)                       # integrate over circle
    directivity_linear = 1 / (total_power / (2 * np.pi))             # peak / avg
    directivity_db = 10 * np.log10(directivity_linear)
    return directivity_db

def estimate_gain(D_dB, S11_dB, eta_rad):
    gamma = 10 ** (S11_dB / 20)
    mismatch_eff = 1 - gamma ** 2
    total_eff = eta_rad * mismatch_eff
    G_dB = D_dB + 10 * math.log10(total_eff)
    return G_dB, mismatch_eff, total_eff

def main():
    # === USER INPUTS ===
    S11_dB = -12              # Measured S11 in dB (e.g., -15 dB)
    eta_rad = 0.80            # Radiation efficiency (linear, 0–1)

    # === LOAD AND PROCESS PATTERN ===
    calibration_data = load_calibration()
    angles = sorted(int(k) for k in calibration_data)
    db_values = [calibration_data[str(k)] for k in angles]
    normalized_db = normalize_db_values(db_values)

    # === ESTIMATE DIRECTIVITY ===
    D_dB = estimate_directivity(normalized_db)

    # === ESTIMATE GAIN ===
    G_dB, mismatch_eff, total_eff = estimate_gain(D_dB, S11_dB, eta_rad)

    # === OUTPUT ===
    print(f"\n--- GAIN ESTIMATION ---")
    print(f"Estimated Directivity (D):      {D_dB:.2f} dB")
    print(f"S11 (return loss):             {S11_dB} dB")
    print(f"Reflection efficiency:         {mismatch_eff*100:.1f} %")
    print(f"Radiation efficiency:          {eta_rad*100:.1f} %")
    print(f"Total efficiency (η_total):    {total_eff*100:.1f} %")
    print(f"Estimated Gain (G):            {G_dB:.2f} dB\n")

if __name__ == "__main__":
    main()
