from turtle import *
from random import uniform

# Color stuff
colors = {9: (20, 21, 23), 8: (30, 36, 22), 7: (41, 52, 22), 6: (52, 67, 21),
          5: (63, 83, 21), 4: (73, 98, 20), 3: (84, 114, 20), 2: (95, 129, 19),
          1: (108, 145, 19)}
colormode(255)

# Animation speed
speed("fastest")

# Drawing logic
def drawTree(point, angle, depth):
    penup()
    setpos(point)
    if depth:
        pencolor(colors[depth])
        pensize(depth + 10 * 2**(depth - 9) + 4**(2 - depth))
        setheading(angle)
        pendown()
        forward(10 * depth)
        new_point = position()
        # New branch parametrisation
        tilt_left = uniform(10, 30)
        tilt_right = uniform(10, 30)
        drawTree(new_point, angle - tilt_right, depth - 1)
        drawTree(new_point, angle + tilt_left, depth - 1)

# Actual work
drawTree((0, -200), 90, 9)
exitonclick()
