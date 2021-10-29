from locust import HttpUser, task, between


class ProjectPerfTest(HttpUser):
    wait_time = between(1, 5)

    @task
    def index_page(self):
        self.client.get("/")

    @task
    def summary(self):
        self.client.post("/showSummary", {"email": "john@simplylift.co"})

    @task
    def book(self):
        self.client.get('/book/Test Competition/Simply Lift')

    @task(3)
    def purchase_places(self):
        data = {"places": "3",
                "competition": "Test Competition",
                "club": "Simply Lift"
        }
        self.client.post('/purchasePlaces', data=data)

    @task
    def display_points_board(self):
        self.client.get('/pointsBoard')