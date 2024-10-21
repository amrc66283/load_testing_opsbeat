from locust import HttpUser, TaskSet, task, between
import time

class UserBehavior(TaskSet):
    def on_start(self):
        self.username = "sahil@dglide.com"
        self.password = "sahil@dglide.com"
        
        # Perform login and store the token
        self.headers = {
            "Authorization": f"Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ3ZmUifQ.Gy4CY4DTnmvMgdXS61PTIV530oKxG_i95fOlJ3CrxaTP5xH3o5qijvOxGAGi077nRenXPYfnf9lLyhvGdQsjOQ",
            "X-TenantID" : "tenant3"
        }
        self.login()        
        # Variable to store the last created ticket's ID
        self.created_ticket_id = None

    def rest_api_call(self, url, method, json_body=None, headers=None):
        if method.lower() == "post":
            response = self.client.post(url, json=json_body, headers=headers)
        elif method.lower() == "put":
            response = self.client.put(url, json=json_body, headers=headers)
        elif method.lower() == "get":
            response = self.client.get(url, headers=headers)
        elif method.lower() == "delete":
            response = self.client.delete(url, headers=headers, json = json_body)
        else:
            raise ValueError("Unsupported HTTP method")
        
        return response.json()
    
    def login(self):
        """ Function to log in and return the token. """
        url = "/api/v1/user/login"
        json_body = {
            "username": self.username,
            "password": self.password
        }
        response = self.rest_api_call(url, "post", json_body=json_body, headers=self.headers)
        return response.get("result", {}).get("tokenDetail", {}).get("token")

    @task
    def getAllModules(self):
        url = "/api/v1/module"  
        response = self.rest_api_call(url, "get", headers=self.headers)
        print(response.get("statusCode"))
        
    @task
    def fetchStarDeskModule(self):
        url = "/api/v1/form/module/39"  
        response = self.rest_api_call(url, "get", headers=self.headers)
        print(response.get("statusCode"))
        
    @task
    def getTicketDetails(self):
        url = "/api/v1/form/name/ticket"  
        response = self.rest_api_call(url, "get", headers=self.headers)
        print(response.get("statusCode"))
        
    @task
    def xyz(self):
        url = "/api/v1/field/form/258"  
        response = self.rest_api_call(url, "get", headers=self.headers)
        print(response.get("statusCode"))

    @task
    def pqr(self):
        url = "/api/v1/action/form/258"  
        response = self.rest_api_call(url, "get", headers=self.headers)
        print(response.get("statusCode"))

    @task
    def asa(self):
        url = "/api/v1/field/form/258"  
        response = self.rest_api_call(url, "get", headers=self.headers)
        print(response.get("statusCode"))

    @task
    def search(self):
        url = "/api/v1/table/ticket/data/search"  
        response = self.rest_api_call(url, "post",
                                      json_body= {
                                                    "pagination": {
                                                        "pageSize": 20,
                                                        "page": 0
                                                    },
                                                    "where": [],
                                                    "sort": []
                                                    }, headers=self.headers)
        print(response.get("statusCode"))

        
    @task
    def getPreferences(self):
        url = "/api/v1/form/258/field/preference"  
        response = self.rest_api_call(url, "get", headers=self.headers)
        print(response.get("statusCode"))


    @task
    def updateTicketActual(self):
        for i in range(10):
            url = "https://leadgen-api.dglide.com/api/v1/table/ticket/data/save" , 
            response = self.rest_api_call(url, "put",
                                        json_body= {
                                                    "uuid" : "22b8c8cf-e2ea-40ef-9f85-94045f77e3df",
                                                    "status": "1",
                                                    "priority": "1",
                                                    "requester": "000a76f8-a4a7-4ce3-9e38-a3a1a52e5830",
                                                    "summary": str(i) + "th time updating the ticket",
                                                    "description" : "test"
                                                    }, headers=self.headers)
            print(response.get("statusCode"))
            print("ticket updated")
            
            
    def create_ticket(self):
        """ Function to create a ticket via API. """
        url = "/api/v1/table/ticket/data/save"
        json_body = {
            "subject": "summary",
            "status" : "1",
            "priority" : "1",
            "description": "locust load testing going on...",
            "requester": "00009578-ce47-45fa-bd5a-3b0da5bb832c" 
        }
       
        response = self.rest_api_call(url, "post", json_body=json_body, headers=self.headers)
        self.created_ticket_id = response.get("result").get("uuid")
        print(f"Created Ticket ID: {self.created_ticket_id}")

    def delete_ticket(self):
        """ Function to delete the last created ticket via API. """
        if self.created_ticket_id:
            url = "/api/v1/table/ticket/data"
            listOfTickets = []
            listOfTickets.append(self.created_ticket_id)
            self.rest_api_call(url, "delete", headers=self.headers, json_body = listOfTickets)
            self.created_ticket_id = None  # Reset the ticket ID after deletion
            print("deleted successfully")
    @task
    def run_ticket_cycle(self):
        """ Run the ticket creation and deletion in a cycle every minute. """
        if self.created_ticket_id:
            self.delete_ticket()
        self.create_ticket()

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)

    def tick(self):
        current_time = int(time.time())
        if current_time % 60 == 0:
            self.user_behavior.run_ticket_cycle()
