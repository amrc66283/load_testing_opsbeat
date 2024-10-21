from locust import HttpUser, TaskSet, task, between
import time

class UserBehavior(TaskSet):
    def on_start(self):
        self.username = "sysadmin@example.com"
        self.password = "sysadmin"
        
        # Perform login and store the token
        self.token = self.login()
        self.headers = {
            "Authorization": f"Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJzeXNhZG1pbkBleGFtcGxlLmNvbSJ9.51pNq4WnXSYf3yN4md0LhUdHUTg9E8cmTJPeRaWM_oF-gTKQ4-Mcq_vM_s7FhTOiwMxJj0FNGxDEI1w3Ek1obQ",
        }
        
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
        response = self.rest_api_call(url, "post", json_body=json_body)
        return response.get("result", {}).get("tokenDetail", {}).get("token")

    @task
    def getAllModules(self):
        url = "/api/v1/module"  
        response = self.rest_api_call(url, "get", headers=self.headers)
        print(response.get("statusCode"))
        
    @task
    def fetchStarDeskModule(self):
        url = "/api/v1/form/module/38"  
        response = self.rest_api_call(url, "get", headers=self.headers)
        print(response.get("statusCode"))
        
    @task
    def getTicketDetails(self):
        url = "/api/v1/form/name/ticket"  
        response = self.rest_api_call(url, "get", headers=self.headers)
        print(response.get("statusCode"))
        
    @task
    def xyz(self):
        url = "/api/v1/field/form/242"  
        response = self.rest_api_call(url, "get", headers=self.headers)
        print(response.get("statusCode"))

    @task
    def pqr(self):
        url = "/api/v1/action/form/242"  
        response = self.rest_api_call(url, "get", headers=self.headers)
        print(response.get("statusCode"))

    @task
    def asa(self):
        url = "/api/v1/field/form/242"  
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
        url = "/api/v1/form/242/field/preference"  
        response = self.rest_api_call(url, "get", headers=self.headers)
        print(response.get("statusCode"))


    @task
    def updateTicketActual(self):
        for i in range(10):
            url = "https://leadgen-api.dglide.com/api/v1/table/ticket/data/save" , 
            response = self.rest_api_call(url, "put",
                                        json_body= {
                                                    "uuid" : "00072dff-7a0e-457d-b7a8-87a6c422aab1",
                                                    "status": "1",
                                                    "priority": "1",
                                                    "requester": "00009578-ce47-45fa-bd5a-3b0da5bb832c",
                                                    "summary": str(i) + "th time updating the ticket",
                                                    "description" : "test"
                                                    }, headers=self.headers)
            print(response.get("statusCode"))
            print("ticket updated")

    @task
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
        print(response)
        self.created_ticket_id = response.get("result").get("uuid")
        print(f"Created Ticket ID: {self.created_ticket_id}")

    @task
    def delete_ticket(self):
        """ Function to delete the last created ticket via API. """
        if self.created_ticket_id:
            url = "/api/v1/table/ticket/data"
            listOfTickets = []
            listOfTickets.append(self.created_ticket_id)
            response = self.rest_api_call(url, "delete", headers=self.headers, json_body = listOfTickets)
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
