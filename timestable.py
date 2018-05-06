from turtle import *
from math import pi, sin, cos

# Constants
txt_h = 12
radius = 320
txt_w = 50
modulus = 100

# Set up a drawing turtle and a turtle for text positioning
turtle = Turtle()
text_turtle = Turtle()
text_turtle.hideturtle()
text_turtle.penup()

# Draw initial circle, position text turtle
turtle.penup()
turtle.setpos(0,-radius)
text_turtle.setpos(+txt_h/4, -radius-3*txt_h)
text_turtle.speed("fastest")
text_turtle.color("red")
turtle.pendown()
turtle.circle(radius)

# Draw nodes and text
for i in range(modulus):
    turtle.dot(12)
    text_turtle.write(i, align="center", font=("Arial", 12, "bold"))
    turtle.circle(radius, 360/modulus)
    text_turtle.circle(radius+2*txt_h, 360/modulus)

# Coordinates on the circle
def coords_from_int(n):
    return [radius * sin(n/modulus*2*pi),
            -radius * cos(n/modulus*2*pi)]

# Get input
operand = int(numinput("Einmaleins.", "Reihe:", 3, minval=2, maxval=10))

# Do the actual math
turtle.color("blue")
visited = set()
for a in range(modulus):
    result = a
    turtle.penup()
    turtle.setpos(*coords_from_int(result))
    while result not in visited:
        visited.add(result)
        result = (result * operand) % modulus
        turtle.pendown()
        turtle.setpos(*coords_from_int(result))

done()
