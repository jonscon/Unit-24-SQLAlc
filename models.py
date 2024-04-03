"""Models for Blogly."""

import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

# MODELS GO BELOW
class User(db.Model):
    """User."""
    
    __tablename__ = "users"

    def __repr__(self):
        u = self
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)    
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(200), nullable=True, default=DEFAULT_IMAGE_URL)
    
    # delete-orphan deletes all posts that a user created if that user is deleted
    posts = db.relationship('Post', cascade='all, delete-orphan', 
                            backref="user")

class Post(db.Model):
    """Post."""

    __tablename__ = "posts"

    def __repr__(self):
        p = self
        return f"<Post id={p.id} title={p.title} content={p.content} created_at={p.created_at} user_id={p.user_id}>"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, 
                           nullable=False, 
                           default=datetime.datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    tags = db.relationship('Tag', secondary="posts_tags", backref="posts")

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")

class Tag(db.Model):
    """Tag."""

    __tablename__ = "tags"

    def __repr__(self):
        t = self
        return f"<Tag id={t.id} name={t.name}>"
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    name = db.Column(db.Text, nullable=False, unique=True)

class PostTag(db.Model):
    """Joins Post and Tag tables."""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id', ondelete='SET NULL'), nullable=True, primary_key=True)
    
    tag_id = db.Column(db.Integer, db.ForeignKey(
        'tags.id', ondelete='SET NULL'), nullable=True, primary_key=True)