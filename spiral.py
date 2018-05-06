from turtle import *
from colorsys import hsv_to_rgb

N = 55
speed(0)
bgcolor("black")
for j in reversed(range(N)):
    color(hsv_to_rgb(j/N, 1, 1))
    circle(5*j)
    circle(-5*j)
    left(j/2)

exitonclick()
