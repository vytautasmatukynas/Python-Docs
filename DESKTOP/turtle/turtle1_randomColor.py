from turtle import Turtle, Screen
import random


sample = Turtle()
sample.shape("turtle")


colours = ["red", "blue", "yellow", "black"]


def draw(num_sides):
    angle = 360/ num_sides
    for i in range(num_sides):
        sample.forward(100)
        sample.right(angle)

for shape_sides in range(2, 15):
    sample.color(random.choice(colours))
    draw(shape_sides)

screen = Screen()
screen.exitonclick()