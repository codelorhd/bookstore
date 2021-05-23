from locust import task
from locust import HttpUser, between


# ALWAYS USE THE TEST DATABASE WHEN RUNNING LOAD TEST
# E.G. set TESTING = True
# uvicorn run:app --reload --port 3000
class BookstoreLoadTest(HttpUser):
    # host = "http://localhost:3000"
    host = "http://143.244.222.147"

    @task
    def token_test(self):
        self.client.post("/token", dict(username="Solomon", password="password"))

    @task
    def test_post_user(self):
        user_dict = {
            "name": "Solomon",
            "password": "1234",
            "role": "ADMIN",
            "mail": "a@b.com",
        }
        JWT_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJTb2xvbW9uIiwiZXhwaXJhdGlvbiI6MTYyMjIzODAyNC44MDk5ODksInJvbGUiOiJBRE1JTiJ9.PSf7L9PISb7uuLJssq4gEnTB8-rVAhNoW3468gEhr8M"
        auth_header = {"Authorization": f"Bearer {JWT_TOKEN}"}
        self.client.post("/v1/user", json=user_dict, headers=auth_header)
