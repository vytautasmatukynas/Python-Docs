from turtle import Turtle, Screen
import random


sample = Turtle()
sample.shape("turtle")

# def random_color():
#     r = random.randint(0, 255)
#     g = random.randint(0, 255)
#     b = random.randint(0, 255)
#     color = (r, g, b)
#     return color

colours = ["red", "blue", "yellow", "black"]
directions = [8, 90, 180, 280]
sample.pensize(10)
sample.speed("fastest")

for i in range(100):
    sample.color(random.choice(colours))
    sample.forward(30)
    sample.setheading(random.choice(directions))


screen = Screen()
screen.exitonclick()