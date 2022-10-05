from turtle import width
import matplotlib
import tkinter as tk
from bokeh.plotting import figure, output_file, show, curdoc

# canvas
fig = figure(width=600, height=600)

# movement vector
#vec = ()

def callback():
    pass


# circular cloud
cir = fig.circle([200], [200], size=30, color="black", alpha=0.4)
ds = cir.data_source

# constant movement, constant growth


# instant fallout to ground -> at clouds location

# time needs to be accounted for

show(fig)
