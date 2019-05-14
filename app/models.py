from app import db, loginMgr
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@loginMgr.user_loader
def load_user(id):
    """

    :param id: id of the user
    :return: user object
    """
    try:
        return User.query.get(int(id))
    except:
        return None


class User(UserMixin, db.Model):
    """
    Model for user table
    """
    id = db.Column(db.Integer, primary_key=True)  # define primary key
    name = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    # reference to relationship with posts to access posts of a user and the author of a post directly
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):  # string representation
        return '<User {}>'.format(self.name)

    def set_password(self, pswd):  # set a user password with hash
        self.password_hash = generate_password_hash(pswd)

    def check_password(self, pswd):  # compare entered password with correct password
        return check_password_hash(self.password_hash, pswd)


class Post(db.Model):
    """
    Model for Post table
    """
    id = db.Column(db.Integer, primary_key=True)  # define primary key
    title = db.Column(db.String(64))
    text = db.Column(db.Text(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # foreign key to user id
    # reference to relationship with PostToTag to access posts tags of a post directly
    tags = db.relationship('PostToTag', backref='post', lazy=True)

    def __repr__(self):  # string representation
        return '<Post {}>'.format(self.title)


class PostToTag(db.Model):
    """
    Model for PostToTag table
    """
    id = db.Column(db.Integer, primary_key=True)  # define primary key
    name = db.Column(db.String(64))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)  # foreign key to post id

    def __repr__(self):  # string representation
        return '<PostToTag {}>'.format(self.id)
