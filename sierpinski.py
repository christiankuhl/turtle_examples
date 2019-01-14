from turtle import *
from lsystem import L_System

if __name__ == "__main__":
    system = L_System(start = "F-G-G",
                      production_rules = {"F": "F-G+F+G-F",
                                          "G": "GG"},
                      angle = 120)
    system.exec_map["G"] = system.FORWARD
    speed("fastest")
    tracer(2)
    hideturtle()
    colormode(255)
    pencolor((0, 0, 127))
    bgcolor((0, 0, 0))
    system.draw(iterations = 8,
                base_length = 3,
                initial_heading = 60,
                initial_position = (-400, -300))
    exitonclick()
