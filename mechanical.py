import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# THERMAL PARAMETERS
# -----------------------------
rho = 2330
c = 700
volume = 1e-15
hA = 5e-6

alpha = 2.6e-6
L = 200e-6
theta = np.deg2rad(10)

T_amb = 300
P_on = 0.01

tau = (rho * c * volume) / hA
f_th = 1 / (2 * np.pi * tau)

# -----------------------------
# MECHANICAL PARAMETERS
# -----------------------------
k = 10
m = 1e-9
zeta = 0.05

omega_n = np.sqrt(k / m)
f_mech = omega_n / (2 * np.pi)

# -----------------------------
# FREQUENCY RANGE
# -----------------------------
frequencies = np.logspace(1, 5, 80)
omega = 2 * np.pi * frequencies

# -----------------------------
# THERMAL MODEL (Analytical square-wave)
# -----------------------------
thermal_amp = []

for f in frequencies:
    period = 1 / f
    D = 0.5

    T_on = D * period
    T_off = (1 - D) * period

    A = np.exp(-T_on / tau)
    B = np.exp(-T_off / tau)

    T_max = (P_on / hA) * (1 - A) / (1 - A * B)
    T_min = T_max * B

    deltaT_amp = (T_max - T_min) / 2
    x_amp = alpha * L * deltaT_amp * np.sin(theta)

    thermal_amp.append(x_amp)

thermal_amp = np.array(thermal_amp)
thermal_norm = thermal_amp / np.max(thermal_amp)

# -----------------------------
# MECHANICAL MODEL
# -----------------------------
H_mech = 1 / np.sqrt(
    (1 - (omega / omega_n)**2)**2 +
    (2 * zeta * (omega / omega_n))**2
)

mech_norm = H_mech / np.max(H_mech)

# -----------------------------
# COMBINED RESPONSE
# -----------------------------
combined = thermal_norm * mech_norm
combined_norm = combined / np.max(combined)

# -----------------------------
# PLOTTING
# -----------------------------
plt.figure(figsize=(10, 6))

plt.semilogx(frequencies, thermal_norm, linewidth=2,
             label='Thermal (Square-wave)')

plt.semilogx(frequencies, mech_norm, '--', linewidth=2,
             label='Mechanical (2nd-order)')

plt.semilogx(frequencies, combined_norm, linewidth=2,
             label='Combined Thermo-Mechanical')

# Mark key frequencies
plt.axvline(f_th, linestyle='--', linewidth=1.5,
            label=r'$f_{th} \approx %.0f$ Hz' % f_th)

plt.axvline(f_mech, linestyle=':', linewidth=1.5,
            label=r'$f_{mech} \approx %.0f$ Hz' % f_mech)

plt.xlabel("Frequency (Hz)", fontsize=12)
plt.ylabel("Normalized Displacement (x / x_max)", fontsize=12)
plt.title("Chevron Actuator: Thermal vs Mechanical vs Combined Response", fontsize=13)

plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend()
plt.tight_layout()
plt.show()