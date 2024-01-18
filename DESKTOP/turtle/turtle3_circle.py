from turtle import Turtle, Screen

sample = Turtle()
sample.shape("turtle")


sample.speed("fastest")

for i in range(100):
    sample.circle(100)
    sample.setheading(sample.heading() +10)

screen = Screen()
screen.exitonclick()