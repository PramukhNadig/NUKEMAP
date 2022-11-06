import numpy as np
from matplotlib import pyplot as plt

# Parametric equation of ellipse
# x = u + a(cos(t))
# y = v + b(sin(t))

x = np.linspace(-4,4,9)
y = np.linspace(-5,5,11)

x1, y1 = np.meshgrid(x,y)

random_data = np.random.random((11, 9))
plt.contourf(x1, y1, random_data, cmap="jet")
#plt.colorbar()
plt.savefig("mygraph.png")