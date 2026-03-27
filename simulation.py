import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Parameters
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

frequencies = np.logspace(1, 5, 60)

# -----------------------------
# Simulation settings
# -----------------------------
dt = 2e-6
n_cycles = 6

sim_eff = []
analytical_eff = []

# -----------------------------
# Main loop
# -----------------------------
for f in frequencies:

    period = 1 / f
    t_end = max(n_cycles * period, 5 * tau)
    time = np.arange(0, t_end, dt)

    # -----------------------------
    # SIMULATION
    # -----------------------------
    T = np.zeros_like(time)
    T[0] = T_amb

    for i in range(1, len(time)):
        if (time[i] % period) < (period / 2):
            P_in = P_on
        else:
            P_in = 0

        dTdt = (P_in - hA * (T[i-1] - T_amb)) / (rho * c * volume)
        T[i] = T[i-1] + dTdt * dt

    delta_T = T - T_amb
    x = alpha * L * delta_T * np.sin(theta)

    steady = x[int(0.7 * len(x)):]
    amp_sim = (np.max(steady) - np.min(steady)) / 2

    # -----------------------------
    # ANALYTICAL (Square Wave)
    # -----------------------------
    D = 0.5
    T_on = D * period
    T_off = (1 - D) * period

    A = np.exp(-T_on / tau)
    B = np.exp(-T_off / tau)

    # steady-state amplitude (temperature)
    T_max = (P_on / hA) * (1 - A) / (1 - A * B)
    T_min = T_max * B
    deltaT_amp = (T_max - T_min) / 2

    x_amp_analytical = alpha * L * deltaT_amp * np.sin(theta)

    # -----------------------------
    # NORMALIZATION (same reference)
    # -----------------------------
    delta_T_ref = (P_on * 0.5) / hA
    x_ref = alpha * L * delta_T_ref * np.sin(theta)

    sim_eff.append(amp_sim / x_ref)
    analytical_eff.append(x_amp_analytical / x_ref)

# -----------------------------
# Plot
# -----------------------------
plt.figure(figsize=(9, 5))

plt.semilogx(frequencies, sim_eff, linewidth=2, label='Simulation (Square)')
plt.semilogx(frequencies, analytical_eff, '--', linewidth=2,
             label='Analytical (Square-wave model)')

plt.axvline(f_th, linestyle='--', linewidth=1.5,
            label=r'$f_{th} \approx %.0f$ Hz' % f_th)

plt.xlabel("Frequency (Hz)", fontsize=12)
plt.ylabel("Normalized Efficiency", fontsize=12)
plt.title("Chevron Actuator: Simulation vs Analytical (Square Input)", fontsize=13)

plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend()
plt.tight_layout()
plt.show()