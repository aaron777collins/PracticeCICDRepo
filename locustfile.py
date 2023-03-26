from locust import HttpUser, between, task
import random
import string

import requests

def random_username(length):
    return ''.join(random.choices(string.ascii_letters, k=length))

class MicroblogUser(HttpUser):
    wait_time = between(1, 5)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_start(self):
        self.username, self.password = self.get_credentials()

        # Register a new user
        response = self.client.post("/auth/register", data={
            "username": self.username,
            "email": f"{self.username}@example.com",
            "password": self.password,
            "password2": self.password
        })
        self.cookies = response.cookies


        # Log in with the new user
        response2 = self.client.post("/auth/login", data={
            "username": self.username,
            "password": self.password
        }, cookies=self.cookies)
        self.cookies.update(response2.cookies)

        # Create a post
        self.create_post()


    def get_credentials(self):
        # Generate a random username with a length of 8 characters
        username = random_username(8)
        password = "test"  # Use the same password for all users
        return username, password

    @task
    def view_homepage(self):
        self.client.get("/index")

    @task
    def create_post(self):
        # Include the required form fields for creating a post
        form_data = {
            "testing": "True",
            "post": "This is a test post.",
            "submit": "Submit"
        }
        #Send a POST request to the /index URL
        resp = self.client.post("/index", data=form_data, cookies=self.cookies)
        self.cookies.update(resp.cookies)

    @task
    def view_profile(self):
        self.client.get(f"/user/{self.username}")
