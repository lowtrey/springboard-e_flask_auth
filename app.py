from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import UserForm

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

@app.route("/tweets")
def show_tweets():
  if "user_id" not in session:
    flash("You must login to view this page.")
    return redirect("/")
  return render_template("tweets.html")

# Registration Route
@app.route("/register", methods=["GET", "POST"])
def register_user():
  form = UserForm()
  if form.validate_on_submit():
    username = form.username.data
    password = form.password.data
    new_user = User.register(username, password)

    db.session.add(new_user)
    db.session.commit()
    session["user_id"] = new_user.id
    flash("Welcome! Successfully Created Your Account!")
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
      flash(f"Welcome Back, {user.username}!")
      session["user_id"] = user.id
      return redirect("/tweets")
    else:
      form.username.errors = ["Invalid username / password."]

  return render_template("login.html", form=form)

# Logout Route (Convention is POST request)
@app.route("/logout")
def logout_user():
  session.pop("user_id")
  flash("Goodbye!")
  return redirect("/")