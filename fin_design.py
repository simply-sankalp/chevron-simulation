# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

# # ----------------------------
# # Parameters (edit these)
# # ----------------------------
# h = 20            # Heat transfer coefficient (W/m^2K)
# k = 130           # Thermal conductivity (Silicon ~130 W/mK)
# w = 10e-6         # Width of fin (10 microns)

# # ----------------------------
# # Variable ranges
# # ----------------------------
# L = np.linspace(10e-6, 200e-6, 50)   # Length: 10 µm to 200 µm
# t = np.linspace(1e-6, 20e-6, 50)     # Thickness: 1 µm to 20 µm

# L_grid, t_grid = np.meshgrid(L, t)

# # ----------------------------
# # Compute parameters
# # ----------------------------
# A_c = w * t_grid
# P = 2 * (w + t_grid)

# m = np.sqrt(h * P / (k * A_c))

# # Avoid division by zero
# mL = m * L_grid
# mL[mL == 0] = 1e-12

# # Fin efficiency
# eta = np.tanh(mL) / mL

# # ----------------------------
# # Plot
# # ----------------------------
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# ax.plot_surface(L_grid * 1e6, t_grid * 1e6, eta)

# # Labels
# ax.set_xlabel('Length (µm)')
# ax.set_ylabel('Thickness (µm)')
# ax.set_zlabel('Fin Efficiency')

# plt.title('Fin Efficiency vs Length and Thickness')
# plt.show()

import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# Parameters
# ----------------------------
h = 20            # W/m^2K
k = 130           # W/mK (Silicon)
w = 10e-6         # width (fixed)

# ----------------------------
# Variable ranges
# ----------------------------
L = np.linspace(10e-6, 900e-6, 100)
t = np.linspace(1e-6, 50e-6, 100)

L_grid, t_grid = np.meshgrid(L, t)

# ----------------------------
# Fin properties
# ----------------------------
A_c = w * t_grid
P = 2 * (w + t_grid)

m = np.sqrt(h * P / (k * A_c))
mL = m * L_grid
mL[mL == 0] = 1e-12

# Efficiency
eta = np.tanh(mL) / mL

# Surface area (approx, excluding tip)
A_f = 2 * L_grid * (w + t_grid)

# "Usefulness" = proportional to total heat dissipation
Q = eta * A_f

# Normalize Q for visualization
Q_norm = Q / np.max(Q)

# ----------------------------
# Plotting
# ----------------------------
fig, ax = plt.subplots(figsize=(8,6))

# Contour for efficiency
cont1 = ax.contour(L_grid * 1e6, t_grid * 1e6, eta, levels=10)
ax.clabel(cont1, inline=True, fontsize=8)

# Contour for usefulness
cont2 = ax.contour(L_grid * 1e6, t_grid * 1e6, Q_norm, levels=10, linestyles='dashed')
ax.clabel(cont2, inline=True, fontsize=8)

# Labels
ax.set_xlabel('Length (µm)')
ax.set_ylabel('Thickness (µm)')
ax.set_title('Design Map: Efficiency (solid) vs Heat Dissipation (dashed)')

plt.show()