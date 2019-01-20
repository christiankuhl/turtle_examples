from turtle import *
import colorsys

def colour_wheel(x=0, y=0, r=200, phi=0, instance=None):
    angle = ((towards((x, y)) + phi) % 360) / 360
    radius = distance((x, y)) / 200
    colour_rgb = colorsys.hsv_to_rgb(angle, radius, 1)
    pencolor(int(255 * min(1, max(c, 0))) for c in colour_rgb)

def colour_table(table, instance):
    pencolor(table.get(str(instance.level()), (255, 255, 255)))

def tree_width(instance):
    depth = 9 - instance.level()
    pensize(depth + 10 * 2**(depth - 9) + 4**(2 - depth))
