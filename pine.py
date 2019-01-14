from turtle import *
from lsystem import L_System

if __name__ == "__main__":
    system = L_System(start = "SLFFF",
                      production_rules = {"S": "[+++G][---G]<TS",
                                          "G": "<+H[-G]L",
                                          "H": "<-G[+H]L",
                                          "T": "TL",
                                          "L": "[-FFF][+FFF]F"},
                      angle = 18,
                      scale_factor = 1.2)
    speed("fastest")
    tracer(200)
    hideturtle()
    colormode(255)
    pencolor((41, 52, 22))
    bgcolor((0, 0, 0))
    pensize(5)
    system.draw(iterations = 9,
                base_length = 20,
                initial_heading = 90,
                initial_position = (0, -350))
    exitonclick()
