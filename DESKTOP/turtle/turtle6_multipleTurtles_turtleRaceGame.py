import random
from turtle import Turtle, Screen

race_on = False
screen = Screen()
screen.setup(width=500, height=400)
bet = screen.textinput(title="Choose", prompt="Which turtle will win the race red/blue/green: ")

colors = ['red', "blue", "green"]
y_pos = [-100, 0, 100]
all_turtles = []

for index in range(0, 3):
    new_turtle = Turtle(shape="turtle")
    new_turtle.penup()
    new_turtle.color(colors[index])
    new_turtle.goto(x=-200, y=y_pos[index])
    all_turtles.append(new_turtle)

if bet:
    race_on = True

while race_on:
    for turtle in all_turtles:
        if turtle.xcor() > 230:
            race_on = False
            wining_color = turtle.pencolor()
            if wining_color == bet:
                print("You won!")
            else:
                print("Try again.")

        random_dist = random.randint(0, 10)
        turtle.forward(random_dist)

screen.exitonclick()
