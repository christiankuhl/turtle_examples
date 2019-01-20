import sys
from lsystem import L_System
from collections import OrderedDict
from functools import partial
import json
import render_hooks
import turtle

def draw_example(name, example_file="lsystem_examples.json"):
    with open(example_file, "r") as file:
        all_examples = json.load(file, object_hook=OrderedDict)
    try:
        example = all_examples[name]
    except KeyError:
        raise KeyError(f"No example with name '{name}' found!'")
    try:
        example_system = example["lsystem"]
    except KeyError:
        raise AttributeError(f"No L-system definition for example '{name}' found!'")
    draw_options = example.get("draw_options", {})
    hook_candidates = draw_options.get("render_hooks", [])
    if hook_candidates:
        draw_options["render_hooks"] = []
    for hook_def in hook_candidates:
        hook_name, *args = hook_def
        render_hook = getattr(render_hooks, hook_name)
        render_hook = partial(render_hook, *args)
        draw_options["render_hooks"].append(render_hook)
    turtle_options = example.get("turtle_options", {})
    for option in turtle_options.get("pre", []):
        for function, args in option.items():
            getattr(turtle, function)(*args)
    system = L_System(**example_system)
    system.draw(**draw_options)
    for option in turtle_options.get("post", []):
        for function, args in option.items():
            getattr(turtle, function)(*args)

if __name__ == "__main__":
    try:
        example_name = sys.argv[1]
    except IndexError:
        example_name = input("Example name: ")
    turtle.setup(width=960, height=810)
    turtle.speed("fastest")
    turtle.tracer(2)
    turtle.hideturtle()
    turtle.colormode(255)
    turtle.bgcolor((0, 0, 0))
    turtle.pencolor((255, 255, 255))
    turtle.pensize(1)
    draw_example(example_name)
    turtle.exitonclick()
