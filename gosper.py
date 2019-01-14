from turtle import *
from lsystem import L_System
import colorsys

def set_colour():
    angle = towards((0, 0)) / 365
    radius = distance((0, 0)) / 300
    colour = []
    colour_rgb = colorsys.hsv_to_rgb(angle, radius, 1)
    for c in colour_rgb:
        c *= 255
        c = int(c)
        colour.append(c)
    pencolor(colour)

if __name__ == "__main__":
    system = L_System(start = "XF",
                      production_rules = {"X": "X+YF++YF-FX--FXFX-YF+",
                                          "Y": "-FX+YFYF++YF+FX--FX-Y"},
                      angle = 60)
    speed("fastest")
    tracer(2)
    hideturtle()
    colormode(255)
    bgcolor((0, 0, 0))
    system.draw(iterations = 5,
                base_length = 4,
                initial_heading = 0,
                initial_position = (150, -250),
                render_hook = set_colour)
    exitonclick()
