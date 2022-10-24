import matplotlib.pyplot as plt
from matplotlib import animation

'''
Basic model parameters
    - circular cloud
    - constant movement
    - constant growth
    - instant fall out -> at clouds location
    - account for time somehow

V2 model parameters
    - miller based cloud shape/growth
    - fallout is a gradient
    - cloud fallout stops at some point
'''

# parameters
radii_growth = 0.50             # how fast the cloud grows
movement_speed = 0.02           # speed of cloud
movement_direction = [1, 1]     # x and y direction on 2d graph
fallout_interval = 2            # frequency of fallout readings
fallout_opacity = 0.1           # opacity of fallout patches

# for displayed animations, duration is 0.001 * frames * interval
fallout_duration = 3            # how many seconds fallout will last
fps = 10                        # how much of a gamer you are
frames = 100                    # total frames of the animation
fallout_timer = fallout_duration * fps 

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
    if i % fallout_interval == 0 and i < fallout_timer:
        ax.add_patch(
            plt.Circle((x, y), 
                currRad, 
                color='black', 
                alpha=fallout_opacity
            )
        )    

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
    frames = frames,
    init_func=init,
    interval=1000,
    blit=True,
)

anim.save('output.gif', dpi=100, writer=animation.PillowWriter(fps=fps))
fig.savefig('output.png')
plt.show()
