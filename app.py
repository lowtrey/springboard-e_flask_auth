from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///auth_demo"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)

# db.drop_all()
# db.create_all()

@app.route("/")
def show_index():
  return render_template("index.html")