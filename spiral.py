from turtle import *

spiral = Turtle()

i = 0
while True:
    i += 1
    spiral.forward(i * 10)
    spiral.right(144)
    if abs(spiral.pos()) > 400:
        break

done()
