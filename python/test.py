import math
from matplotlib import animation, patches
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from matplotlib.collections import PatchCollection

############################ Parameters #######################################
# cloud parameters
radii_growth = 0.50                 # how fast the cloud grows
movement_speed = 0.02               # speed of cloud
movement_direction = [1, 1]         # x and y direction on 2d graph

# color parameters
limit_black = 0.6                   # max fallout value (limits darkness)
limit_white = 0.9                   # minimum fallout value (limits whiteness)
blend_weight = 0.1                  # how much weight is given to new overlapped pixels

# fallout parameters
fallout_interval = 10               # frequency of fallout readings
fallout_opacity = 0.1               # opacity of fallout patches
fallout_duration = 10               # how many seconds fallout will last

# animation parameters
fps = 10                            # how much of a gamer you areobjects
frames = 100                        # total frames of the animation 
###############################################################################

# # initalize the figure
fig = plt.figure()
ax = fig.add_subplot(111)
plt.xlim([-100, 100])
plt.ylim([-100, 100])

# the cloud
patch = plt.Circle((0, 0), 1)
fallout_timer = fallout_duration * fps
fallout_count = math.ceil(fallout_timer/fallout_interval) # number of fallout plots

patch_dict = {}         # maps coordinates to patch objects
patch_storage = []      # stores patch objects
fc_storage = []         # stores pixel colors

def init():
    ax.add_patch(patch)
    return patch,

def create_patch(x, y, color):
    return patches.Rectangle(
        (x, y),
        width = 1,
        height = 1,
        color = str(max(limit_black, color)),
        edgecolor = None,
        alpha = 1
    )

def modify_patch():
    pass

def animate(i):
    x, y = patch.center
    r = patch.radius  

    if i % fallout_interval == 0 and i < fallout_timer:
        instance = int(i/fallout_interval) + 1
        print(f"Drawing fallout instance {instance} of {fallout_count}")

        dist_dict = defaultdict(lambda: [])
        pixel_dict = defaultdict(lambda: [])
        patch_collection = []
        fc = []

        # iterates through each pixel, like a square
        for row in range(int(x-r), int(x+r)):
            for col in range(int(y-r), int(y+r)):

                # compute distance of current coordinates from origin
                dist = math.sqrt((x-row)**2 + (y - col)**2) 

                # if its within the circle since we're iterating like a square
                if dist <= r:
                    color = round(dist / r, 2) # color is computed based on distance from origin

                    dist_dict[color].append(dist)
                    pixel_dict[color].append((row, col))

                    if color <= limit_white: 
                        if f"{row},{col}" not in patch_dict: 
                           new_patch = create_patch(row, col, color)
                           patch_collection.append(new_patch)
                           fc.append(str(max(limit_black, color)))
                           patch_dict[f"{row},{col}"] = (instance -1, len(patch_collection)-1)

                        else:
                            # compute new color
                             a, b = patch_dict[f"{row},{col}"]
                             old_color = float(fc_storage[a][b])

                             # how the blending works
                             new_color = str(max(0,old_color - color*blend_weight))
                             fc_storage[a][b] = new_color
                             curr_pc = patch_storage[a]
                             curr_pc.set_facecolors(fc_storage[a])

        # update everything 
        pc = PatchCollection(patch_collection, facecolor=fc)
        ax.add_collection(pc)
        patch_storage.append(pc)
        fc_storage.append(fc)

    # cloud movement
    x = i+(movement_speed * movement_direction[0])
    y = i+(movement_speed * movement_direction[0])
    patch.center = (x, y)

    # cloud growth 
    patch.set_radius(r + radii_growth)

    return patch,

anim = animation.FuncAnimation(
    fig,
    animate,
    frames = frames,
    init_func=init,
    interval=1000,
    blit=True,
)

anim.save('output.gif', dpi=500, writer=animation.PillowWriter(fps=fps))
fig.savefig('outpuuuut.png')
plt.show()
