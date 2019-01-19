from turtle import *
from lsystem import L_System
import colorsys

def set_colour():
    angle = towards((150, 0)) / 365
    radius = distance((150, 0)) / 200
    colour_rgb = colorsys.hsv_to_rgb(angle, radius, 1)
    pencolor(int(255 * min(1, max(c, 0))) for c in colour_rgb)

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
