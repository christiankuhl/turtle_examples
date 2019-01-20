from turtle import *
import re
from functools import partial
from numpy.random import choice, random

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
       &	         Increment the line length by line length increment
       %	         Decrement the line length by line length increment
       >	         Multiply the line length by the line length scale factor
       <	         Divide the line length by the line length scale factor
       *	         Multiply the line width by the line width scale factor
       /	         Divide the line width by the line width scale factor
       (	         Decrement turning angle by turning angle increment
       )	         Increment turning angle by turning angle increment

    These replacement rules are provided to the constructor via production_rules,
    which is expected to be of type dict(str: str | dict(float: str))).
    So in the simplest case, production_rules is a mapping from strings to strings.
    If, on the other hand, the values of production_rules are dict(float: str),
    the keys of these values are interpreted as weights for a random choice of
    a production rule at any stage.
    Additional alphabet characters can be provided by providing additional_actions,
    or by monkeypatching self.exec_map, which handles the mapping of alphabet
    characters to instance methods. Symbols which are neither contained in above
    list nor in additional_actions are interpreted as NO_OP.
    Further, each concrete drawing method may depend on other parameters such
    as scale factors etc., which can be passed to the constructor as optional
    parameters.
    Finally, for the draw method, there is a hook called before each rendering
    step which can be used for graphics customisation.
    """
    def __init__(self, start, production_rules, angle, scale_factor=1,
                 width_increment=0, angle_increment=0, length_increment=0,
                 additional_actions={}, condense=True, debug=False, **kwargs):
        self.start = start
        self.productions = production_rules
        self.angle = angle
        self.scale_factor = scale_factor
        self.width_increment = width_increment
        self.length_increment = length_increment
        self.angle_increment = angle_increment
        self.kwargs = kwargs
        self.stack = []
        self.debug = debug
        self.reductions = {sym: repl for (sym, repl) in production_rules.items()
                                                if len(sym) > len(repl)}
        self.exec_map = {"X": self.NO_OP,
                         "F": self.FORWARD,
                         "f": self.FORWARD_NODRAW,
                         "|": self.REVERSE,
                         "#": self.INC_WIDTH,
                         "!": self.DEC_WIDTH,
                         ">": self.MUL_LENGTH,
                         "<": self.DIV_LENGTH,
                         "*": self.MUL_WIDTH,
                         "/": self.DIV_WIDTH,
                         "&": self.INC_LENGTH,
                         "%": self.DEC_LENGTH,
                         "[": self.LBRACKET,
                         "]": self.RBRACKET,
                         "+": self.PLUS,
                         "-": self.MINUS,
                         "(": self.INC_ANGLE,
                         ")": self.DEC_ANGLE}
        self.condense_result = condense
        for symbol, (action, args) in additional_actions.items():
            if len(symbol) > 1:
                print(f"W: Symbol of length {len(symbol)} encountered.\
                      Symbol skipped.")
            try:
                action = partial(getattr(self, action), *args)
            except AttributeError:
                print(f"W: Action {action} is not defined - mapped to NO_OP.")
                action = self.NO_OP
            self.exec_map[symbol] = action
        for symbol, operation in self.exec_map.items():
            if operation == self.NO_OP:
                self.reductions[symbol] = ""
        for symbol in self.start:
            if self.exec_map.get(symbol, self.NO_OP) == self.NO_OP:
                self.reductions[symbol] = ""
        self.simple = True
        for production in production_rules.values():
            if type(production) == str:
                for symbol in production:
                    if self.exec_map.get(symbol, self.NO_OP) == self.NO_OP:
                        self.reductions[symbol] = ""
            elif issubclass(type(production), dict):
                self.simple = False
                for rule in production.values():
                    for symbol in production:
                        if self.exec_map.get(symbol, self.NO_OP) == self.NO_OP:
                            self.reductions[symbol] = ""
            else:
                raise ValueError("Cannot interpret production rules.")
    def execute_productions(self, iterations=5, productions=None, start_string=""):
        if not productions:
            productions = self.productions
        if not start_string:
            start_string = self.start
        if self.simple or not iterations:
            result = self.execute_simple_productions(iterations, productions, start_string)
        else:
            result = self.execute_prob_productions(iterations, productions, start_string)
        return result
    def execute_simple_productions(self, iterations, productions, start_string):
        production_regex = re.compile("|".join(map(re.escape, productions.keys())))
        result = start_string
        if iterations:
            for _ in range(iterations):
                result = production_regex.sub(lambda match: productions[match.group(0)], result)
        else:
            while True:
                old_result = result
                result = production_regex.sub(lambda match: productions[match.group(0)], result)
                if old_result == result:
                    break
        return result
    def execute_prob_productions(self, iterations, productions, start_string):
        result = start_string
        for _ in range(iterations):
            prob_productions = self.probabilistic_productions(productions)
            production_regex = re.compile("|".join(map(re.escape, prob_productions.keys())))
            result = production_regex.sub(lambda match: prob_productions[match.group(0)], result)
        return result
    def probabilistic_productions(self, productions):
        result = {}
        for key, value in productions.items():
            if type(value) == str:
                result[key] = value
            else:
                total_weight = sum(float(w) for w in value.keys())
                chosen_value = choice(list(value.values()), p=[float(weight)/total_weight
                                                         for weight in value.keys()])
                result[key] = chosen_value
        return result
    def draw(self, iterations, base_length=5, initial_heading=0,
             initial_position=(0, 0), render_hooks=[]):
        self.length = base_length
        penup()
        setheading(initial_heading)
        setpos(*initial_position)
        pendown()
        production_string = self.execute_productions(iterations)
        if self.condense_result:
            production_string = self.condense(production_string)
        if self.debug:
            print(production_string)
        for symbol in production_string:
            for hook in render_hooks:
                hook(self)
            self.exec_map.get(symbol, self.NO_OP)()
    def condense(self, production_string):
        result = self.execute_productions(None, self.reductions, production_string)
        return result
    def level(self):
        return len(self.stack)
    def NO_OP(self):
        pass
    def FORWARD(self):
        forward(self.length)
    def FORWARD_NODRAW(self):
        penup()
        forward(self.length)
        pendown()
    def LBRACKET(self):
        self.stack.append((position(), heading(), self.length, pensize()))
    def RBRACKET(self):
        pos, head, length, pen = self.stack.pop()
        penup()
        setpos(pos)
        setheading(head)
        self.length = length
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
    def MUL_LENGTH(self):
        self.length *= self.scale_factor
    def DIV_LENGTH(self):
        self.length /= self.scale_factor
    def INC_LENGTH(self):
        self.length += self.length_increment
    def DEC_LENGTH(self):
        self.length -= self.length_increment
    def INC_ANGLE(self):
        self.angle += self.angle_increment
    def DEC_ANGLE(self):
        self.angle -= self.angle_increment
    def CIRCLE(self, radius=None, extent=None, steps=None):
        if not radius:
            radius = self.radius
        circle(radius, extent, steps)
    def RANDOM_ANGLE(self, left, right):
        setheading(heading() + (right - left) * random() + left)
