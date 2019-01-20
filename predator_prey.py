from turtle import Turtle, speed, exitonclick, tracer, bgcolor, speed
from numpy.random import random

PREDATORS = 2
PREY = 12

class Animal(Turtle):
    def __init__(self, id, position, heading):
        super(Animal, self).__init__()
        self.id = id
        self.dead = False
        self.saturated = False
        self.penup()
        self.setpos(position)
        self.setheading(heading)
        self.pendown()
        self.pencolor(self.__class__.COLOR)
    def register(self, predators, prey):
        self.predators = predators
        self.prey = prey
    def turn(self, heading):
        heading = heading % 360
        curr_heading = self.heading() % 360
        angle_diff = curr_heading - heading
        if abs(angle_diff)  < 180:
            turn_angle = angle_diff
        elif angle_diff <= -180:
            turn_angle = angle_diff + 360
        else:
            turn_angle = angle_diff - 360
        if abs(turn_angle) > self.__class__.TURN_SPEED:
            if turn_angle < 0:
                turn_angle = -self.__class__.TURN_SPEED
            else:
                turn_angle = self.__class__.TURN_SPEED
        self.setheading(self.heading() - turn_angle)
    def run(self):
        self.forward(self.__class__.RUN_SPEED)

class Predator(Animal):
    RUN_SPEED = 6
    TURN_SPEED = 10
    ATTACK_SUCCESS = .85
    LOSE_INTEREST = 300
    COLOR = "red"
    def move(self):
        if self.saturated:
            return
        available_prey = sorted((p for p in self.prey.values()
                                if self.distance(p) < Predator.LOSE_INTEREST),
                                                key=lambda q: self.distance(q))
        if not available_prey:
            return
        nearest = available_prey[0]
        heading = self.towards(nearest)
        self.turn(heading)
        near_prey = [p for p in self.prey.values() if self.distance(p) < Predator.RUN_SPEED]
        if near_prey:
            nearest = sorted(near_prey, key=lambda q: self.distance(q))[0]
            self.attack(nearest)
        else:
            self.run()
    def attack(self, other):
        if random() < Predator.ATTACK_SUCCESS:
            self.saturated = True
            other.dead = True
            self.prey.pop(other.id)
            self.predators.pop(self.id)

class Prey(Animal):
    RUN_SPEED = 5
    TURN_SPEED = 60
    PREDATOR_LENGTHS = 15
    ZIGZAG_PROBABILITY = .125
    COLOR = "blue"
    def move(self):
        if self.dead or not self.predators:
            return
        nearest = sorted((p for p in self.predators.values()), key=lambda q: self.distance(q))[0]
        heading = self.towards(nearest) + 180
        self.turn(heading)
        near_predator = [p for p in self.predators.values() if self.distance(p) < Prey.PREDATOR_LENGTHS * Predator.RUN_SPEED]
        if near_predator:
            self.zigzag()
        self.run()
    def zigzag(self):
        if random() >= Prey.ZIGZAG_PROBABILITY:
            return
        if random() < 1/2:
            self.turn(self.heading() - 90)
        else:
            self.turn(self.heading() + 90)
        self.run()

def random_rect(ax, bx, ay, by):
    return ((bx - ax) * random() + ax, (by - ay) * random() + ay, )

if __name__ == "__main__":
    bgcolor("black")
    tracer(2)
    # tracer(PREY + PREDATORS)
    predators = {}
    prey = {}
    for id in range(PREDATORS):
        predators[id] = Predator(id, random_rect(-400, -200, -400, -200), 90 * random())
    for id in range(PREY):
        prey[id] = Prey(id, random_rect(-200, -100, -200, -100), 360 * random())
    animals = list(predators.values()) + list(prey.values())
    for p in animals:
        p.register(predators, prey)
    for _ in range(500):
        for p in animals:
            p.move()
    exitonclick()
