from locust import task
from locust import HttpUser, between


# ALWAYS USE THE TEST DATABASE WHEN RUNNING LOAD TEST
# E.G. set TESTING = True
# uvicorn run:app --reload --port 3000
class BookstoreLoadTest(HttpUser):
    host = "http://localhost:3000"

    @task
    def token_test(self):
        self.client.post("/token", dict(username="user2", password="secret"))

    @task
    def test_post_user(self):
        user_dict = {
            "name": "Solomon",
            "password": "1234",
            "role": "ADMIN",
            "mail": "a@b.com",
        }
        auth_header = {
            "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyMiIsImV4cGlyYXRpb24iOjE2MjIxOTcwNTIuMDI2MzIxLCJyb2xlIjoiQURNSU4ifQ.N962imbWj4lamJ9bCYMSVZJaBPUACmKWzm3pf6kiwDk"
        }
        self.client.post("/v1/user", json=user_dict, headers=auth_header)
