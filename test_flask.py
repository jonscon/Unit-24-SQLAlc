from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_test_db'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()
        Post.query.delete()

        user = User(first_name="Test", last_name="User")
        db.session.add(user)
        db.session.commit()

        post = Post(title="My First Post",
                    content="This is my first post.",
                    user_id=user.id)
        db.session.add(post)
        db.session.commit()

        self.user_id= user.id
        self.user = user
        self.post_id = post.id
        self.post = post

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test", html)
            self.assertIn("User", html)

    def test_show_user_details(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Test User</h1>', html)
            self.assertIn("My First Post", html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "Test", "last_name": "User2", 
                "image_url": "https://www.shutterstock.com/image-vector/url-shortener-man-pushes-address-bar-2201694049"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test User2", html)

    def test_edit_user(self):
        with app.test_client() as client:
            d = {"first_name": "Test", "last_name": "UserChanged",
                 "image_url": "https://www.shutterstock.com/image-vector/url-shortener-man-pushes-address-bar-2201694049"}

            resp = client.post(f"/users/{self.user_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test UserChanged", html)

    def test_add_post(self):
        with app.test_client() as client:
            d = {"title": "My Second Post", "content": "Just another post",
                 "user_id": 1}
            resp = client.post(f"/users/{self.user_id}/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("My Second Post", html)

    def test_edit_post(self):
        with app.test_client() as client:
            d = {"title": "Post Changed", "content": "Did it work?",
                 "user_id": self.user_id}

            resp = client.post(f"/posts/{self.post_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Post Changed", html)