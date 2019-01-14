from turtle import *
import re


class L_System:
    """
    Implements a basic Lindenmayer system for drawing with the turtle module.
    An instance is minimally created by providing a start string as well as a
    set of production rules, i.e. a dictionary of replacement rules for symbols
    of the following alphabet:

    Character        Meaning
       X             Do nothing
       F	         Move forward by line length drawing a line
       f	         Move forward by line length without drawing a line
       +	         Turn left by turning angle
       -	         Turn right by turning angle
       |	         Reverse direction (ie: turn by 180 degrees)
       [	         Push current drawing state onto stack
       ]	         Pop current drawing state from the stack
       #	         Increment the line width by line width increment
       !	         Decrement the line width by line width increment
       >	         Multiply the line length by the line length scale factor
       <	         Divide the line length by the line length scale factor
       (	         Decrement turning angle by turning angle increment
       )	         Increment turning angle by turning angle increment

    Additional alphabet characters can be provided by monkeypatching self.exec_map,
    which handles the mapping of alphabet characters to instance methods.
    Symbols not contained in above list are interpreted as NOOP.
    Further, each concrete drawing method may depend on other parameters such
    as scale factors etc., which can be passed to the constructor as optional
    parameters.
    Finally, for the draw method, there is a hook called after each rendering
    step which can be used for graphics customisation.
    """
    def __init__(self, start, production_rules, angle, scale_factor=1,
                 width_increment=0, angle_increment=0, **kwargs):
        self.start = start
        self.productions = production_rules
        self.angle = angle
        self.scale_factor = scale_factor
        self.width_increment = width_increment
        self.angle_increment = angle_increment
        self.kwargs = kwargs
        self.stack = []
        self.exec_map = {"X": self.NOOP,
                         "F": self.FORWARD,
                         "f": self.FORWARD_NODRAW,
                         "|": self.REVERSE,
                         "#": self.INC_WIDTH,
                         "!": self.DEC_WIDTH,
                         ">": self.MUL_WIDTH,
                         "<": self.DIV_WIDTH,
                         "[": self.LBRACKET,
                         "]": self.RBRACKET,
                         "+": self.PLUS,
                         "-": self.MINUS,
                         "(": self.INC_ANGLE,
                         ")": self.DEC_ANGLE}
    def FORWARD(self):
        forward(self.length)
    def FORWARD_NODRAW(self):
        penup()
        forward(self.length)
        pendown()
    def NOOP(self):
        pass
    def LBRACKET(self):
        self.stack.append((position(), heading(), pensize()))
    def RBRACKET(self):
        pos, head, pen = self.stack.pop()
        penup()
        setpos(pos)
        setheading(head)
        pensize(pen)
        pendown()
    def PLUS(self):
        setheading(heading() + self.angle)
    def MINUS(self):
        setheading(heading() - self.angle)
    def REVERSE(self):
        setheading(-heading())
    def INC_WIDTH(self):
        pensize(pensize() + self.width_increment)
    def DEC_WIDTH(self):
        pensize(pensize() - self.width_increment)
    def MUL_WIDTH(self):
        pensize(pensize() * self.scale_factor)
    def DIV_WIDTH(self):
        pensize(pensize() / self.scale_factor)
    def INC_ANGLE(self):
        self.angle += self.angle_increment
    def DEC_ANGLE(self):
        self.angle -= self.angle_increment
    def execute_productions(self, iterations=5):
        production_regex = re.compile("|".join(map(re.escape, self.productions.keys())))
        result = self.start
        for _ in range(iterations):
            result = production_regex.sub(lambda match: self.productions[match.group(0)], result)
        return result
    def draw(self, iterations, base_length=5, initial_heading=0,
             initial_position=(0, 0), render_hook=lambda: None):
        self.length = base_length
        penup()
        setheading(initial_heading)
        setpos(*initial_position)
        pendown()
        production_string = self.execute_productions(iterations)
        for symbol in production_string:
            self.exec_map.get(symbol, self.NOOP)()
            render_hook()
