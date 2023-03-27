from locust import HttpUser, between, task
import random
import string

import requests

from Logger import Logger

def random_username(length):
    return ''.join(random.choices(string.ascii_letters, k=length))

class MicroblogUser(HttpUser):
    wait_time = between(1, 5)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sessionID = None
        self.logger = Logger('locustlogs.txt')

    def on_start(self):
        self.username, self.password = self.get_credentials()

        # Register a new user
        with self.client.post("/auth/register", data={
            "username": self.username,
            "email": f"{self.username}@example.com",
            "password": self.password,
            "password2": self.password
        }, catch_response=True) as response:
            # username, email, password, password2
            if response.status_code == 200:
                self.logger.log(f"Registered with username: {self.username}, email: {self.username}@example.com, password: {self.password}", name=self.username)
            else:
                response.failure(f"Failed to register with username:{self.username}, email: {self.username}@example.com, password: {self.password}. Response code: " + str(response.status_code))


        # Log in with the new user
        with self.client.post("/auth/login-api", json={
            "username": self.username,
            "password": self.password
        }, catch_response=True) as response2:
            if response2.status_code == 200:
                self.sessionID = response2.json()["session"]
                self.logger.log(f"Session ID: {self.sessionID}", name=self.username)
                # Create a post
                self.create_post()

            else:
                response2.failure("Failed to login. Response code: " + str(response2.status_code))




    def get_credentials(self):
        # Generate a random username with a length of 8 characters
        username = random_username(8)
        password = "test"  # Use the same password for all users
        return username, password

    @task
    def view_homepage(self):
        with self.client.get("/index", catch_response=True) as resp:
            if resp.status_code == 200:
                self.logger.log("Viewed homepage", name=self.username)
            else:
                resp.failure("Failed to view homepage. Response code: " + str(resp.status_code))

    @task
    def create_post(self):
        # Include the required form fields for creating a post
        headers = {
            "Content-Type": "application/json"
        }
        form_data = {
            "post": "This is a test post.",
            "submit": "Submit"
        }
        #Send a POST request to the /index URL
        with self.client.post("/index-api", headers=headers, json=form_data, cookies={"session": self.sessionID}, catch_response=True) as resp:
            if resp.status_code == 200:
                self.logger.log(f"Created post: {resp.json()}", name=self.username)
            else:
                resp.failure("Failed to create post. Response code: " + str(resp.status_code))

    @task
    def view_profile(self):
        self.client.get(f"/user/{self.username}")
