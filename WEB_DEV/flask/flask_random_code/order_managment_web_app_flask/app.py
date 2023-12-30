from flask import Flask
from datetime import timedelta


# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = "my secret key"
# Session lifetime
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=300)

# Import blueprints
from views.login import login_bp
from views.errors import error_pages
from views.edit import edit_table
from views.table import main_table

# Register blueprints
app.register_blueprint(main_table)
app.register_blueprint(edit_table)
app.register_blueprint(error_pages)
app.register_blueprint(login_bp)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
