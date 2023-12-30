from flask_login import UserMixin
from project import db, login_manager


################################ LOGIN ###############################
@login_manager.user_loader
def load_user(id):
    return UserModel.query.get(id)

login_manager.login_view = "log.login"
#############################################################################

##################################### MODELS #############################################
class UserModel(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    posts = db.relationship('PostModel', backref='author', lazy='dynamic')

    # data user should provide to create record. ID will be generated auto.
    def __init__(self, user, password):
        self.user = user
        self.password = password

    def __repr__(self):
        return f"username: {self.user}, password: {self.password}"


class PostModel(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    subtitle = db.Column(db.String(80), unique=True, nullable=False)
    text = db.Column(db.String(300), nullable=False)
    post_date = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(), nullable=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # data user should provide to create record. ID will be generated auto.
    def __init__(self, title, subtitle, text, post_date, image, user_id):
        self.title = title
        self.subtitle = subtitle
        self.text = text
        self.post_date = post_date
        self.image = image
        self.user_id = user_id

    def __repr__(self):
        return f"title: {self.title}, subtitle: {self.subtitle},  date: {self.post_date}, user: {self.user_id}, image: {self.image}"