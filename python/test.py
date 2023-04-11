import matplotlib.pyplot as plt
from matplotlib import animation
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

# print(data)

current_data = data[0]

# for displayed animations, duration is 0.001 * frames * interval
fallout_duration = 10            # how many seconds fallout will last
fps = 10                        # how much of a gamer you are
frames = 100                    # total frames of the animation
fallout_timer = fallout_duration * fps 

# parameters
radii_growth = 0.50                  # how fast the cloud grows
movement_direction = [1, 0]          # x and y direction on 2d graph
fallout_interval = 2                 # frequency of fallout readings
fallout_opacity = [0.8]                # opacity of fallout patches
stem_circle_radius = current_data["x_center"] - current_data["upwind_stem_distance"]              # initial size of cloud
max_stem_width = current_data["max_stem_width"]            # maximum width of the stem
max_cloud_width = current_data["max_cloud_width"]                  # maximum cloud width
ground_zero = [0, 0]                 # initial ground zero location
x_center = [current_data["x_center"], 0]
# upwind_stem_distance = current_data["upwind_stem_distance"]
# downwind_stem_distance = current_data["downwind_stem_distance"]
upwind_cloud_distance = [current_data["upwind_cloud_distance"], 0]      # location of the start of the stem
cloud_widen_point = [current_data["cloud_widen_point"], 0]          # point where cloud reaches max width
downwind_cloud_distance = [current_data["downwind_cloud_distance"], 0]    # final destination
ground_upwind_growth = (max_stem_width - stem_circle_radius) / (frames * (upwind_cloud_distance[0] / downwind_cloud_distance[0]))
upwind_widen_growth = (max_cloud_width - max_stem_width) / (frames * ((cloud_widen_point[0] - upwind_cloud_distance[0]) / downwind_cloud_distance[0]))
widen_downwind_growth = (stem_circle_radius - max_cloud_width) / (frames * ((downwind_cloud_distance[0] - cloud_widen_point[0]) / downwind_cloud_distance[0]))
movement_speed = downwind_cloud_distance[0] / frames

print(upwind_cloud_distance[0])
print(cloud_widen_point[0])
print(downwind_cloud_distance[0])

# initalize the figure
fig = plt.figure()
ax = fig.add_subplot(111)
plt.xlim([-100, downwind_cloud_distance[0] + 100])
plt.ylim([max_cloud_width * -1 - 100, max_cloud_width + 100])

# the cloud
patch = plt.Circle((ground_zero[0], ground_zero[1]), stem_circle_radius)

def init():
    ax.add_patch(patch)
    return patch,

def animate(i):
    x, y = patch.center
    currRad = patch.radius  # Affects radius

    # fallout readings
    # if i % fallout_interval == 0 and i < fallout_timer and x <= 90:
    #     ax.add_patch(
    #         plt.Circle((x, y), 
    #             currRad, 
    #             color='black', 
    #             alpha=fallout_opacity[0]
    #         )
    #     )    
    ax.add_patch(
        plt.Circle((x, y),
                    currRad,
                    color='black',
                    alpha=fallout_opacity[0]))

    # cloud movement
    # x += (movement_speed * movement_direction[0])
    x += movement_speed
    y += 0

    patch.center = (x, y)

    # cloud growth
    if x < upwind_cloud_distance[0]:
        patch.set_radius(currRad + ground_upwind_growth)
        print(x, 'upwind', currRad, i)
        fallout_opacity[0] = 0.5
    elif x < cloud_widen_point[0]:
        patch.set_radius(currRad + upwind_widen_growth)
        print(x, 'widen', currRad, i)
        fallout_opacity[0] = 0.2
    elif x < downwind_cloud_distance[0]:
        patch.set_radius(currRad + widen_downwind_growth)
        print(x, 'downwind', currRad, i)
        fallout_opacity[0] = 0.1

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
