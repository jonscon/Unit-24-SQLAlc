"""Seed file to make sample data for db."""

from models import User, Post, Tag, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# Make a bunch of users
test_user = User(first_name="Short", last_name="URL", image_url="https://t.ly/5Y4YW")
sponge = User(first_name="Spongebob", last_name="Squarepants", image_url="https://t.ly/LXR4T")
db.session.add_all([test_user, sponge])
db.session.commit()

# Make a bunch of posts
post1 = Post(title="My First Post", content="This is my first post.", user_id=1)
post2 = Post(title="My Second Post", content="This is my second post.", user_id=1)
post3 = Post(title="Bikini Bottom", content="Who lives in a pineapple under the sea?", user_id=2)
post4 = post1 = Post(title="Patrick Star", content="Patrick stinks.", user_id=2)
db.session.add_all([post1, post2, post3, post4])
db.session.commit()

# Make a bunch of tags
tag1 = Tag(name="Nickelodeon")
tag2 = Tag(name="Short User")
post1.tags.append(tag2)
post2.tags.append(tag2)
post3.tags.append(tag1)
post4.tags.append(tag1)

db.session.commit()
