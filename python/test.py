import math
from matplotlib import animation, patches
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from matplotlib.collections import PatchCollection

# parameters
radii_growth = 0.50                 # how fast the cloud grows
movement_speed = 0.02               # speed of cloud
movement_direction = [1, 1]         # x and y direction on 2d graph
alpha_offset = 1.2                  # transparency offset
color_norm = 0.9
fallout_interval = 10               # frequency of fallout readings
fallout_opacity = 0.1               # opacity of fallout patches
fallout_duration = 10               # how many seconds fallout will last
fps = 10                            # how much of a gamer you are
frames = 100                        # total frames of the animation
fallout_timer = fallout_duration * fps 

# # initalize the figure
fig = plt.figure()
ax = fig.add_subplot(111)
plt.xlim([-100, 100])
plt.ylim([-100, 100])

# the cloud
patch = plt.Circle((0, 0), 1)

# dictionary storing all patches
patch_dict = {}

patch_storage = []
fc_storage = []

def init():
    ax.add_patch(patch)
    return patch,

def animate(i):
    x, y = patch.center
    r = patch.radius  

    # offset for computing distanced
    offset_x = x - int(x)
    offset_y = y - int(y)
    offset_rad = r - int(r)

    drawings = math.ceil(fallout_timer/fallout_interval)




    # fallout readings
    if i % fallout_interval == 0 and i < fallout_timer:
        instance = int(i/fallout_interval) + 1
        print(f"Drawing fallout instance {instance} of {drawings}")
        alpha_offset = 0.3 * (0.5 ** (instance-1))

        # for loop can only iterate through integers
        # so to compute distance, need to store decimal offset
        # offset_x = x - int(x)
        # offset_y = y - int(y)
        # offset_rad = r - int(r)

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

                    # how to do transparency
                    # well black is 0, white is 1
                    # white should be less transparent
                    

                    # transparency could also be adjusted based on the color too
                    # if the color is near white, don't bother drawing the pixel
                    if color <= color_norm: 
                        
                        if f"{row},{col}" not in patch_dict: 
                          
                           new_patch = patches.Rectangle(
                                (row, col),
                                1,
                                1,
                                color=str(max(0.6, color)),
                                edgecolor = None,
                                alpha=1

                            )
                           patch_collection.append(new_patch)
                           fc.append(str(max(0.6, color)))
   
                           patch_dict[f"{row},{col}"] = (instance -1, len(patch_collection)-1)
                        else:
                            # compute new color
                             a, b = patch_dict[f"{row},{col}"]
                             old_color = float(fc_storage[a][b])

                             # how the blending works
                             diff = 1 - 0.6
                             weight = 0.1
                             new_color = str(max(0,old_color - color*weight))
                             fc_storage[a][b] = new_color
                             curr_pc = patch_storage[a]
                             curr_pc.set_facecolors(fc_storage[a])


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


'''
you can access patches through the patch collection after they're drawn
all the drawn patches are stored in patch collections
but each patch collection is a circle
meaning we need to figure out the right patch_collection and then the index within
the dictionary can store the index locations
dictionary key is x,y coordinate -> index of the 2d array where it is stored
can retrieve the color and then update it!
'''