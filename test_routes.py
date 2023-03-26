import random
import string
from flask_login import login_user, current_user
import pytest
import requests
from app import create_app, db
from app.models import Post, User
from tests import TestConfig

# creates app contexts and then removes it later
@pytest.fixture(scope="module")
def app_contexts():
    app = create_app(TestConfig)
    app_context = app.app_context()
    app_context.push()
    db.create_all()
    yield app, app_context
    db.session.remove()
    db.drop_all()
    app_context.pop()

# Returns a registered user and the credentials to login (user, username, password)
@pytest.fixture(scope="module")
def registeredUser():
    user = User(username="john", email="john@example.com")
    user.set_password("test")
    db.session.add(user)
    db.session.commit()
    return user, "john", "test"

# Creating fixture to mock a post for the test user
@pytest.fixture(scope="module")
def post(registeredUser):
    user, username, password = registeredUser
    post = Post(body="test post", author=user)
    db.session.add(post)
    db.session.commit()
    return post

# @pytest.fixture(scope="module")
# def client(app_contexts):
#     app, app_context = app_contexts
#     return app.test_client()

# Creating test on /updatelikes route
# updatelikes expects:
# {
#     "postId": postId,
#     "increasing": increasing,
#     "page": page
# }
# expect:
# if increasing:
#     return jsonify({"likes": post.like_by(current_user)})
# else:
#     return jsonify({"likes": post.unlike_by(current_user)})
def test_likeby_unlikeby(app_contexts, registeredUser, post):
    app, app_context = app_contexts
    user, username, password = registeredUser
    with app.test_client() as client:
        response = client.post("/auth/login", json={"username": username, "password": password}, follow_redirects=True)
        login_user(user, remember=True)
        # assert response.status_code == 200
        assert current_user.is_authenticated == True
        # when I am logged in and have created a post
        # and I like the post
        post.like_by(current_user)
        # It should increase the likes by 1 (from 0 to 1)
        assert post.likes == 1
        # then if I unlike it
        post.unlike_by(current_user)
        # It should decrease the likes by 1 (from 1 to 0)
        assert post.likes == 0


def test_create_post(app_contexts, registeredUser):
    app, app_context = app_contexts
    user, username, password = registeredUser
    with app.test_client() as client:
# Register a new user

        username = ''.join(random.choices(string.ascii_letters, k=8))
        password = "test"  # Use the same password for all users

        session = requests.Session()

        response = session.post("http://localhost:5000/auth/register", data={
            "username": username,
            "email": f"{username}@example.com",
            "password": password,
            "password2": password
        })

        assert response.status_code == 200
        print(response.cookies)


        # Log in with the new user
        response2 = session.post("http://localhost:5000/auth/login", data={
            "username": username,
            "password": password
        })

        assert response2.status_code == 200
        print(response2.cookies)


        # Create a post
        # Include the required form fields for creating a post
        form_data = {
            "testing": "True",
            "post": "This is a test post.",
            "submit": "Submit"
        }
        #Send a POST request to the /index URL
        resp = session.post("http://localhost:5000/index", data=form_data)

        assert resp.status_code == 200

        assert False
