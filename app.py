"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

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
    
    return render_template("user_form.html")

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
    return render_template("user_detail.html", user=user)

@app.route("/users/<int:user_id>/edit")
def edit_user_page(user_id):
    """Edit a user's information."""
    
    user = User.query.get(user_id)

    return render_template("user_edit.html", user=user)

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

@app.route("/users/<int:user_id>/posts/new")
def add_post_form(user_id):
    """Show form to add post for the user."""

    user = User.query.get(user_id)

    return render_template("add_post.html", user=user)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    """POST method to add post for the user."""

    title = request.form["title"]
    content = request.form["content"]
    
    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show post details."""

    post = Post.query.get(post_id)

    return render_template("post_detail.html", post=post)

@app.route("/posts/<int:post_id>/edit")
def edit_post_form(post_id):
    """Form to edit post details."""

    post = Post.query.get(post_id)

    return render_template("post_edit.html", post=post)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """POST method to edit post details."""

    post = Post.query.get(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post.id}")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete post."""

    user_id = Post.query.get(post_id).user_id
    Post.query.filter_by(id=post_id).delete()
    
    db.session.commit()

    return redirect(f"/users/{user_id}")