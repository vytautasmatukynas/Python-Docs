from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def get_visitor_ip():
    visitor_ip = request.remote_addr
    return f"Visitor's IP address is: {visitor_ip}"

if __name__ == '__main__':
    app.run(debug=True)