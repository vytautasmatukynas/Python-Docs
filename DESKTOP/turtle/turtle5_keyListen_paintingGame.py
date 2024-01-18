from turtle import Turtle, Screen

sample = Turtle()
sample.shape("turtle")
screen = Screen()


def move_forward():
    sample.forward(10)
    # sample.setheading(90)


def move_backward():
    # sample.forward(10)
    # sample.setheading(270)
    sample.backward(10)


def move_left():
    # sample.forward(10)
    # sample.setheading(180)
    newheading = sample.heading() + 10
    sample.setheading(newheading)


def move_right():
    # sample.forward(10)
    # sample.setheading(360)
    newheading = sample.heading() - 10
    sample.setheading(newheading)


screen.listen()
screen.onkey(key="w", fun=move_forward)
screen.onkey(key="s", fun=move_backward)
screen.onkey(key="a", fun=move_left)
screen.onkey(key="d", fun=move_right)

screen.exitonclick()
