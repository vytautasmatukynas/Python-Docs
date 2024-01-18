from turtle import Screen
import time
from turtle7_snakeClass import Snake
from turtle7_foodClass import food
from turtle7_scoreClass import scoreBoard

screen = Screen()
screen.setup(width=600, height=600)

screen.bgcolor("black")
screen.title("Gyvačiukas")
screen.tracer(0)

snake = Snake()
food = food()
scoreborad = scoreBoard()

screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")

TIME_COUNT = 0.1

game_on = True

while game_on:
    screen.update()
    time.sleep(TIME_COUNT)

    snake.move()

    # detect collision with food
    if snake.head.distance(food) < 15:
        food.refresh()
        snake.extend()
        scoreborad.increase_score()
        TIME_COUNT -= 0.001

    # detect collision with wall
    if snake.head.xcor() > 280 or snake.head.xcor() < -280 or \
        snake.head.ycor() > 280 or snake.head.ycor() < -280:
        scoreborad.reset()
        snake.reset()


    # detect collision with tale
    for segment in snake.snake_seg[1:]:
        if snake.head.distance(segment) < 10:
            scoreborad.reset()
            snake.reset()


screen.exitonclick()
