from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
  """Connect to database"""
  db.app = app
  db.init_app(app)


class User(db.Model):

  __tablename__ = "users"

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)

  username = db.Column(db.Text, unique=True, nullable=False)

  password = db.Column(db.Text, nullable=False)

  @classmethod
  def register(cls, username, password):
    """Register user with hashed password & return user."""

    hashed = bcrypt.generate_password_hash(password)
    # Turn bytestring into normal (unicode utf8) string
    hashed_utf8 = hashed.decode("utf8")

    # Return instance of user with username & hashed password
    return cls(username=username, password=hashed_utf8)

  @classmethod
  def authenticate(cls, username, password):
    """Validate user and password."""

    user = User.query.filter_by(username=username).first()
    valid_password = bcrypt.check_password_hash(user.password, password)

    if user and valid_password:
      # Return user instance
      return user
    else:
      return False

class Tweet(db.Model):

  __tablename__ = "tweets"

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)

  text = db.Column(db.Text, nullable=False)

  user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

  user = db.relationship("User", backref="tweets")