"""Seed file to make sample data for db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# Make a bunch of departments
test_user = User(first_name="Short", last_name="URL", image_url="https://t.ly/5Y4YW")
sponge = User(first_name="Spongebob", last_name="Squarepants", image_url="https://t.ly/LXR4T")
db.session.add_all([test_user, sponge])

db.session.commit()
