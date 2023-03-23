import numpy as np
import matplotlib.pyplot as plt

# Define constants
Q = 100 # Emission rate (kg/s)
u = 10 # Wind speed (m/s)
sigmay = 10 # Lateral dispersion (m)
sigmaz = 5 # Vertical dispersion (m)
y0 = 0 # Lateral distance (m)
z0 = 10 # Height (m)
x0 = 0 # Longitudinal distance (m)
sigmax = 20 # Longitudinal dispersion (m)

def gaussian(x, y, sigma_x, sigma_y):
    return np.exp(-((x-x0)**2) / (2 * sigma_x**2) - ((y-y0)**2) / (2 * sigma_y**2)) / (2 * np.pi * sigma_x * sigma_y)

x = np.linspace(-100, 100, 1000)
y = np.linspace(-100, 100, 1000)
X, Y = np.meshgrid(x, y)
Z = gaussian(X, Y, sigmax, sigmay)
C = (Q / (2 * np.pi * u * sigmax * sigmay * sigmaz)) * Z * np.exp(-(z0**2) / (2 * sigmaz**2))

fig, ax = plt.subplots()
ax.imshow(C, extent=[x.min(), x.max(), y.min(), y.max()])
ax.set_xlabel('Longitudinal distance (m)')
ax.set_ylabel('Lateral distance (m)')
ax.set_title('Gaussian Plume')

plt.savefig('plume.png')
