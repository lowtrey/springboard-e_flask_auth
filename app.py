from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Tweet
from sqlalchemy.exc import IntegrityError
from forms import UserForm, TweetForm
import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "postgresql:///auth_demo")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "abc123")
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)

# db.drop_all()
# db.create_all()

@app.route("/")
def show_index():
  return render_template("index.html")

@app.route("/tweets", methods=["GET", "POST"])
def show_tweets():
  if "user_id" not in session:
    flash("You must login to view this page.", "danger")
    return redirect("/")
    
  form = TweetForm()
  all_tweets = Tweet.query.all()

  if form.validate_on_submit():
    text = form.text.data
    new_tweet = Tweet(text=text, user_id=session["user_id"])
    db.session.add(new_tweet)
    db.session.commit()
    flash("Tweet Created!", "success")
    return redirect("/tweets")
    
  return render_template("tweets.html", form=form, tweets=all_tweets)

# Delete Tweet Route
@app.route("/tweets/<int:id>", methods=["POST"])
def delete_tweet(id):
  """Delete Tweet"""
  # Make sure user is logged in.
  if "user_id" not in session:
    flash("Please login first.", "danger")
    return redirect("/login")
  else:
    tweet = Tweet.query.get_or_404(id)
    if tweet.user_id == session["user_id"]:
      db.session.delete(tweet)
      db.session.commit()
      flash("Tweet Deleted!", "info")
      return redirect("/tweets")
    else:
      flash("You don't have permission to do that.", "danger")
      return redirect("/tweets")

# Registration Route
@app.route("/register", methods=["GET", "POST"])
def register_user():
  form = UserForm()
  if form.validate_on_submit():
    username = form.username.data
    password = form.password.data
    new_user = User.register(username, password)

    db.session.add(new_user)
    # Handle Error if username already exists
    try:
      db.session.commit()
    except IntegrityError:
      form.username.errors.append("Username taken, please choose another")
      return render_template("register.html", form=form)
      
    session["user_id"] = new_user.id
    flash("Welcome! Successfully Created Your Account!", "success")
    return redirect("/tweets")
  else:
    return render_template("register.html", form=form)

# Login Route
@app.route("/login", methods=["GET", "POST"])
def login_user():
  form = UserForm()
  if form.validate_on_submit():
    username = form.username.data
    password = form.password.data
    user = User.authenticate(username, password)
    if user:
      flash(f"Welcome Back, {user.username}!", "primary")
      session["user_id"] = user.id
      return redirect("/tweets")
    else:
      form.username.errors = ["Invalid username / password."]

  return render_template("login.html", form=form)

# Logout Route (Convention is POST request)
@app.route("/logout")
def logout_user():
  session.pop("user_id")
  flash("Goodbye!", "info")
  return redirect("/")