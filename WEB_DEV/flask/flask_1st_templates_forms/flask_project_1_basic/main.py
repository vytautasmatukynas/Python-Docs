from flask import Flask
import random


app = Flask(__name__)

number = random.randint(0, 9)
print(number)

@app.route("/")
def main_window():
    return "<h1>Guess a number between 0 and 9</h1>" \
           "<img src='https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif'>"

@app.route("/<int:guess_number>")
def quess(guess_number):
    if guess_number < number:
        return "<h1 style={color: red}>TOO LOW</h1>" \
               "<img src='https://media1.giphy.com/media/XJLEXP9xEJRevqXxnR/200w.webp?cid=ecf05e47pt8eu2k5gn4yrv2w520mtfpm5zmc5vnpudo4alh1&rid=200w.webp&ct=g'>"
    elif guess_number > number:
        return "<h1 style={color: red}>TOO HIGH</h1>" \
               "<img src='https://media2.giphy.com/media/3o6nUYik7Vi8Fe0swg/giphy.webp'>"
    else:
        return "<h1 style={color: green}>CORRECT!!!</h1>" \
               "<img src='https://media3.giphy.com/media/8zILIhf3MfpyRwwPZC/giphy.webp'>"

# # SAME RESULT.
# @app.py.route("/<guess_number>")
# def quess(guess_number):
#     if int(guess_number) < int(number):
#         return "<h1 style={color: red}>TOO LOW</h1>" \
#                "<img src='https://media1.giphy.com/media/XJLEXP9xEJRevqXxnR/200w.webp?cid=ecf05e47pt8eu2k5gn4yrv2w520mtfpm5zmc5vnpudo4alh1&rid=200w.webp&ct=g'>"
#     elif int(guess_number) < int(number):
#         return "<h1 style={color: red}>TOO HIGH</h1>" \
#                "<img src='https://media2.giphy.com/media/3o6nUYik7Vi8Fe0swg/giphy.webp'>"
#     else:
#         return "<h1 style={color: green}>CORRECT!!!</h1>" \
#                "<img src='https://media3.giphy.com/media/8zILIhf3MfpyRwwPZC/giphy.webp'>"


if __name__ == "__main__":
    app.run()