from turtle import *
from lsystem import L_System
import colorsys

def set_colour():
    angle = towards((0, 0)) / 365
    radius = distance((0, 0)) / 200
    colour_rgb = colorsys.hsv_to_rgb(angle, radius, 1)
    pencolor(int(255 * min(1, max(c, 0))) for c in colour_rgb)

if __name__ == "__main__":
    system = L_System(start = "A",
                      production_rules = {"A": "-BF+AFA+FB-",
                                          "B": "+AF-BFB-FA+"},
                      angle = 90)
    speed("fastest")
    tracer(2)
    hideturtle()
    colormode(255)
    bgcolor((0, 0, 0))
    system.draw(iterations = 7,
                base_length = 4,
                initial_heading = 0,
                initial_position = (-250, 250),
                render_hook = set_colour)
    exitonclick()
