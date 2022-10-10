from turtle import width
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import animation
import tkinter as tk

# # movement vector

# # circular cloud

# # constant movement, constant growth

# # instant fallout to ground -> at clouds location

# # time needs to be accounted for

x = [0,1,2]
y = [0,1,2]

fig = plt.figure()
plt.axis("equal")
plt.grid()

ax = fig.add_subplot(111)
ax.set_xlim(-10,10)
ax.set_ylim(-10,10)

patch = plt.Circle((0,0), 1)

def init():
    ax.add_patch(patch)
    return patch,

def animate(i):
    x, y = patch.center
    x = i+1
    y = i+1
    patch.center = (x,y)
    return patch,

anim = animation.FuncAnimation(
    fig, 
    animate, 
    init_func=init,  
    interval=40, 
    blit=True
)

anim.save('output.gif', dpi=100, writer=animation.PillowWriter(fps=30))
plt.show()