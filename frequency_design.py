import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Fixed parameters
# -----------------------------
rho = 2330
c = 700
hA = 5e-6

# Choose representative values
m = 1e-9      # kg

# -----------------------------
# Sweep parameters
# -----------------------------
V_vals = np.logspace(-18, -13, 200)   # volume
k_vals = np.logspace(-2, 2, 200)      # stiffness

V_grid, k_grid = np.meshgrid(V_vals, k_vals)

# -----------------------------
# Compute ratio R = f_th / f_mech
# -----------------------------
thermal_bandwidth = hA / (rho * c * V_grid)
mechanical_bandwidth = np.sqrt(k_grid / m)

R = thermal_bandwidth / mechanical_bandwidth

# -----------------------------
# Plot design map
# -----------------------------
plt.figure(figsize=(9, 6))

# Contour plot
contour = plt.contourf(V_vals, k_vals, np.log10(R), levels=50, cmap='coolwarm')
plt.colorbar(label=r'$\log_{10}(f_{th} / f_{mech})$')

# Boundary line (R = 1)
plt.contour(V_vals, k_vals, R, levels=[1], colors='black', linewidths=2)

# Labels
plt.xscale('log')
plt.yscale('log')

plt.xlabel("Volume (m³)", fontsize=12)
plt.ylabel("Stiffness k (N/m)", fontsize=12)
plt.title("Design Map: Thermal vs Mechanical Limitation", fontsize=13)

# Region annotations
plt.text(1e-17, 1e1, "Thermal-limited", color='white', fontsize=11)
plt.text(1e-14, 1e-1, "Mechanical-limited", color='white', fontsize=11)

plt.grid(True, which='both', linestyle='--', linewidth=0.5)

plt.tight_layout()
plt.show()