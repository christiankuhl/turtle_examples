from turtle import *
from lsystem import L_System

if __name__ == "__main__":
    system = L_System(start = "X",
                      production_rules = {"X": "F+[[X]-X]-F[-FX]+X",
                                          "F": ">F<F"},
                      angle = 25,
                      scale_factor=1.2)
    speed("fastest")
    tracer(200)
    hideturtle()
    colormode(255)
    pencolor((41, 52, 22))
    bgcolor((0, 0, 0))
    pensize(1)
    system.draw(iterations = 8,
                base_length = 1.2,
                initial_heading = 65,
                initial_position = (-300, -350))
    exitonclick()
