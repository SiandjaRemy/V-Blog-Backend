from locust import HttpUser, between, task


class BlogUser(HttpUser):
    wait_time = between(5, 15)

    def __init__(self, parent):
        super(BlogUser, self).__init__(parent)
        self.token = ""
    
    def on_start(self):
        with self.client.post("/auth/jwt/create/", {"email": "admin@gmail.com", "password": "1111"}) as response:
            self.token = response.json()["access"]
            print(self.token)

        self.headers = {
            "Authorization": f"Token {self.token}",
            # "Content-Type": "application/json",
        }
    
    @task
    def index(self):
        self.client.get("/blog/posts/", headers=self.headers)
