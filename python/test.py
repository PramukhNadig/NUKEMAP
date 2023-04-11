import math
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation, patches
from matplotlib.collections import PatchCollection
import json

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

with open('fallout_output.json', 'r') as f:
  data = json.load(f)

def filterNone(e):
    if e != None:
        return True
    else:
        return False

data = list(filter(filterNone, data))

current_data = data[0]

# for displayed animations, duration is 0.001 * frames * interval
fallout_duration = 10                                                                             # how many seconds fallout will last
fps = 10                                                                                          # how much of a gamer you are
frames = 100                                                                                      # total frames of the animation


# parameters
radii_growth = 0.50                                                                               # how fast the cloud grows
movement_direction = [1, 0]                                                                       # x and y direction on 2d graph
fallout_interval = 2                                                                              # frequency of fallout readings
fallout_opacity = [0.8]                                                                           # opacity of fallout patches

# color parameters
limit_black = 0.2                                                                                 # max fallout value (limits darkness)
limit_white = 0.8                                                                                 # minimum fallout value (limits whiteness)
blend_weight = 0.2                                                                                # how much weight is given to new overlapped pixels

stem_circle_radius = current_data["x_center"] - current_data["upwind_stem_distance"]              # initial size of cloud
max_stem_width = current_data["max_stem_width"]                                                   # maximum width of the stem
max_cloud_width = current_data["max_cloud_width"]                                                 # maximum cloud width
ground_zero = [0, 0]                                                                              # initial ground zero location
x_center = [current_data["x_center"], 0]
# upwind_stem_distance = current_data["upwind_stem_distance"]
# downwind_stem_distance = current_data["downwind_stem_distance"]
upwind_cloud_distance = [current_data["upwind_cloud_distance"], 0]                                # location of the start of the stem
cloud_widen_point = [current_data["cloud_widen_point"], 0]                                        # point where cloud reaches max width
downwind_cloud_distance = [current_data["downwind_cloud_distance"], 0]                            # final destination

ground_upwind_growth = (max_stem_width - stem_circle_radius) / (frames * (upwind_cloud_distance[0] / downwind_cloud_distance[0]))
upwind_widen_growth = (max_cloud_width - max_stem_width) / (frames * ((cloud_widen_point[0] - upwind_cloud_distance[0]) / downwind_cloud_distance[0]))
widen_downwind_growth = (stem_circle_radius - max_cloud_width) / (frames * ((downwind_cloud_distance[0] - cloud_widen_point[0]) / downwind_cloud_distance[0]))
movement_speed = downwind_cloud_distance[0] / frames

# initalize the figure
fig = plt.figure()
ax = fig.add_subplot(111)
plt.xlim([-100, downwind_cloud_distance[0] + 100])
plt.ylim([max_cloud_width * -1 - 100, max_cloud_width + 100])
plt.xticks([])
plt.yticks([])

# the cloud
patch = plt.Circle((ground_zero[0], ground_zero[1]), stem_circle_radius)
fallout_timer = fallout_duration * fps 
fallout_count = math.ceil(fallout_timer/fallout_interval) # number of fallout plots

patch_dict = {}         # maps coordinates to patch objects
patch_storage = []      # stores patch objects
fc_storage = []         # stores pixel colors (face colors)

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

def blend_function(old_color, new_color):
    return max(0, old_color - new_color*blend_weight)

def animate(i):
    x, y = patch.center
    r = patch.radius  # Affects radius

    if i % fallout_interval == 0 and i < fallout_timer:
        instance = int(i/fallout_interval) + 1
        print(f"Drawing fallout instance {instance} of {fallout_count}")

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

                    if color <= limit_white: 
                        if f"{row},{col}" not in patch_dict: 
                           patch_collection.append(create_patch(row, col, color))
                           fc.append(str(max(limit_black, color)))
                           patch_dict[f"{row},{col}"] = (instance -1, len(patch_collection)-1)

                        else:
                            # compute new color
                             a, b = patch_dict[f"{row},{col}"]
                             old_color = float(fc_storage[a][b])

                             # how the blending works
                             new_color = str(blend_function(old_color, color))

                             fc_storage[a][b] = new_color
                             patch_storage[a].set_facecolors(fc_storage[a])

        # update everything 
        pc = PatchCollection(patch_collection, facecolor=fc)
        ax.add_collection(pc)
        patch_storage.append(pc)
        fc_storage.append(fc)






    # cloud movement
    # x += (movement_speed * movement_direction[0])
    x += movement_speed
    y += 0
    patch.center = (x, y)

    # cloud growth
    if x < upwind_cloud_distance[0]:
        patch.set_radius(r + ground_upwind_growth)
        # print(x, 'upwind', r, i)
        # fallout_opacity[0] = 0.5
    elif x < cloud_widen_point[0]:
        patch.set_radius(r + upwind_widen_growth)
        # print(x, 'widen', r, i)
        # fallout_opacity[0] = 0.2
    elif x < downwind_cloud_distance[0]:
        patch.set_radius(r + widen_downwind_growth)
        # print(x, 'downwind', r, i)
        # fallout_opacity[0] = 0.1

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
