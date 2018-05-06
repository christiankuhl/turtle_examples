from turtle import *

i = 0
while True:
    i += 1
    forward(i * 10)
    right(144)
    if abs(pos()) > 400:
        break

exitonclick()
