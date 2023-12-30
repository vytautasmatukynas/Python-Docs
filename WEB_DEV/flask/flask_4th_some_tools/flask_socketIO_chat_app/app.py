# Import required modules and classes
from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase

# Create a Flask app.py
app = Flask(__name__)

# Configure a secret key for sessions (used for security)
app.config["SECRET_KEY"] = "hjhjsdahhds"

# Initialize a SocketIO instance linked to the Flask app.py
socketio = SocketIO(app)

# Dictionary to store room information (members and messages)
rooms = {}

# Function to generate a unique room code
def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        
        # Check if generated code is unique
        if code not in rooms:
            break
    
    return code

# Home route for creating/joining a room
@app.route("/", methods=["POST", "GET"])
def home():
    # Clear user's session data
    session.clear()

    # Handle form submissions
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        # Validate user input
        if not name:
            return render_template("home.html", error="Please enter a name.", code=code, name=name)

        if join != False and not code:
            return render_template("home.html", error="Please enter a room code.", code=code, name=name)
        
        room = code

        # Create a new room if requested
        if create != False:
            room = generate_unique_code(4)  # Generate a unique room code
            rooms[room] = {"members": 0, "messages": []}  # Add the room to the rooms dictionary
        elif code not in rooms:
            return render_template("home.html", error="Room does not exist.", code=code, name=name)
        
        # Store user data in the session and redirect to chat room
        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))  # Redirect to the chat room page

    return render_template("home.html")  # Render the home page template

# Chat room route
@app.route("/room")
def room():
    # Retrieve user's session data
    room = session.get("room")
    
    # Redirect to home if session data is missing or room doesn't exist
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))

    # Render the chat room template with room data
    return render_template("room.html", code=room, messages=rooms[room]["messages"])

# SocketIO event handler for receiving messages
@socketio.on("message")
def message(data):
    # Retrieve user's session data
    room = session.get("room")
    
    # Ignore if user is not in a valid room
    if room not in rooms:
        return 
    
    # Prepare message content
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    
    # Broadcast the message to all users in the room
    send(content, to=room)
    
    # Add the message to the room's message history
    rooms[room]["messages"].append(content)
    
    # Print message to server log
    print(f"{session.get('name')} said: {data['data']}")

# SocketIO event handler for user connection
@socketio.on("connect")
def connect(auth):
    # Retrieve user's session data
    room = session.get("room")
    name = session.get("name")
    
    # Ignore if user's session data is incomplete or room doesn't exist
    if not room or not name:
        return
    
    # Disconnect user from room if it no longer exists
    if room not in rooms:
        leave_room(room)
        return
    
    # Add the user to the room and broadcast their entry
    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    
    # Print user's entry to server log
    print(f"{name} joined room {room}")

# SocketIO event handler for user disconnection
@socketio.on("disconnect")
def disconnect():
    # Retrieve user's session data
    room = session.get("room")
    name = session.get("name")
    
    # Remove user from room
    leave_room(room)
    
    # Update room member count and delete room if needed
    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
    
    # Broadcast user's exit message and print to server log
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")

# Run the SocketIO app.py when executed directly
if __name__ == "__main__":
    socketio.run(app, debug=True)
