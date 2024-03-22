"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


connect_db(app)
app.app_context().push()
db.create_all()

app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route("/")
def home_page():
    """Redirect to users page."""
    return redirect("/users")

@app.route("/users")
def show_users():
    """Show users."""

    users = User.query.all()
    return render_template("users.html", users=users)

@app.route("/users/new")
def add_user_form():
    """Create a new user and submit form."""
    
    return render_template("form.html")

@app.route("/users/new", methods=["POST"])
def create_user():
    """POST method to add user to 'users' table."""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show details about a single user."""
    user = User.query.get_or_404(user_id)
    return render_template("detail.html", user=user)

@app.route("/users/<int:user_id>/edit")
def edit_user_page(user_id):
    """Edit a user's information."""
    
    user = User.query.get(user_id)

    return render_template("edit.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """POST method to edit a user's information."""
    
    user = User.query.get(user_id)

    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]
    
    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """POST method to delete a user."""
    
    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect("/users")