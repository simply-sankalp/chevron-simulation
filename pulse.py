import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Physical Parameters
# -----------------------------
rho = 2330
c = 700
volume = 1e-15
hA = 5e-6

alpha = 2.6e-6
L = 200e-6
theta = np.deg2rad(10)

T_amb = 300
P_amp = 0.01   # peak power

tau_th = (rho * c * volume) / hA
f_th = 1 / (2 * np.pi * tau_th)

# -----------------------------
# Frequency sweep
# -----------------------------
frequencies = np.logspace(1, 5, 50)

# -----------------------------
# Waveform definitions
# -----------------------------
def square_wave(t, f):
    return 0.5 * (1 + np.sign(np.sin(2 * np.pi * f * t)))

def sine_wave(t, f):
    return 0.5 * (1 + np.sin(2 * np.pi * f * t))

def triangle_wave(t, f):
    return 0.5 * (1 + (2/np.pi) * np.arcsin(np.sin(2 * np.pi * f * t)))

def sawtooth_wave(t, f):
    return (t * f) % 1  # ramp 0→1

waveforms = {
    "Square": square_wave,
    "Sine": sine_wave,
    "Triangle": triangle_wave,
    "Sawtooth": sawtooth_wave
}

# -----------------------------
# Simulation settings
# -----------------------------
dt = 2e-6
n_cycles = 6

# -----------------------------
# Efficiency storage
# -----------------------------
results = {name: [] for name in waveforms}

# -----------------------------
# Main simulation loop
# -----------------------------
for f in frequencies:

    period = 1 / f
    t_end = max(n_cycles * period, 5 * tau_th)
    time = np.arange(0, t_end, dt)

    for name, waveform in waveforms.items():

        T = np.zeros_like(time)
        T[0] = T_amb

        # Thermal simulation
        for i in range(1, len(time)):
            P_in = P_amp * waveform(time[i], f)
            dTdt = (P_in - hA * (T[i-1] - T_amb)) / (rho * c * volume)
            T[i] = T[i-1] + dTdt * dt

        # Displacement
        delta_T = T - T_amb
        x = alpha * L * delta_T * np.sin(theta)

        # Extract steady-state amplitude
        steady = x[int(0.7 * len(x)):]
        amp = (np.max(steady) - np.min(steady)) / 2

        # Normalize using DC equivalent (mean input = 0.5)
        delta_T_ref = (P_amp * 0.5) / hA
        x_ref = alpha * L * delta_T_ref * np.sin(theta)

        results[name].append(amp / x_ref)

# -----------------------------
# Plotting
# -----------------------------
plt.figure(figsize=(9, 5))

for name, eff in results.items():
    plt.semilogx(frequencies, eff, linewidth=2, label=name)

# Thermal cutoff
plt.axvline(f_th, linestyle='--', linewidth=1.5,
            label=r'$f_{th} \approx %.0f$ Hz' % f_th)

plt.xlabel("Input Frequency (Hz)", fontsize=12)
plt.ylabel("Normalized Efficiency", fontsize=12)
plt.title("Chevron Actuator Efficiency for Different Input Waveforms", fontsize=13)

plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend()
plt.tight_layout()
plt.show()