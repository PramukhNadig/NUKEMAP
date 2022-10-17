import matplotlib.pyplot as plt
from matplotlib import animation

# # movement vector

# # circular cloud

# # constant movement, constant growth

# # instant fallout to ground -> at clouds location

# # time needs to be accounted for

x = [0, 1, 2]
y = [0, 1, 2]
growth = 0.05

fig = plt.figure()
plt.axis("equal")
plt.grid()

ax = fig.add_subplot(111)
ax.set_xlim(-100, 100)
ax.set_ylim(-100, 100)

patch = plt.Circle((0, 0), 1)


def init():
    ax.add_patch(patch)
    return patch,


def animate(i):
    x, y = patch.center
    currRad = patch.radius  # Affects radius

    if i % 20 == 0:
        ax.add_patch(plt.Circle((x, y), currRad))

    x = i+1
    y = i+1
    patch.center = (x, y)
    patch.set_radius(currRad + growth)
    return patch,


anim = animation.FuncAnimation(
    fig,
    animate,
    init_func=init,
    interval=50,
    blit=True,
)

anim.save('output.gif', dpi=100, writer=animation.PillowWriter(fps=500))
plt.show()
