import matplotlib.pyplot as plt
from matplotlib import animation

'''
Basic model parameters
    - circular cloud
    - constant movement
    - constant growth
    - instant fall out -> at clouds location
    - account for time somehow
'''

# parameters
radii_growth = 0.05             # how fast the cloud grows
movement_speed = 1              # speed of cloud
movement_direction = [1, 1]     # x and y direction on 2d graph
fallout_interval = 20           # frequency of fallout readings

# initalize the figure
fig = plt.figure()
ax = fig.add_subplot(111)
plt.xlim([-100, 100])
plt.ylim([-100, 100])

# the cloud
patch = plt.Circle((0, 0), 1)

def init():
    ax.add_patch(patch)
    return patch,

def animate(i):
    x, y = patch.center
    currRad = patch.radius  # Affects radius

    # fallout readings
    if i % fallout_interval == 0:
        ax.add_patch(plt.Circle((x, y), currRad, color='black'))

    # cloud movement
    x = i+(movement_speed * movement_direction[0])
    y = i+(movement_speed * movement_direction[0])
    patch.center = (x, y)

    # cloud growth 
    patch.set_radius(currRad + radii_growth)

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
