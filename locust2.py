from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    def on_start(self):
        """ Perform login when a user starts. """
        # Define single user's credentials
        self.username = "tenant2@example.com"
        self.password = "sysadmin"
        self.tenant_id = "tenant2"
        
        # Perform login and store the token
        self.token = self.login()
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "X-TenantID": self.tenant_id
        }

    def rest_api_call(self, url, method, json_body=None, headers=None):
        """ General function to make REST API calls. """
        if method.lower() == "post":
            response = self.client.post(url, json=json_body, headers=headers)
        elif method.lower() == "get":
            response = self.client.get(url, headers=headers)
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
        headers = {
            "X-TenantID": self.tenant_id
        }
        response = self.rest_api_call(url, "post", json_body=json_body, headers=headers)
        return response.get("result", {}).get("tokenDetail", {}).get("token")

    @task
    def api1(self):
        url = "/api/v1/module"  # Replace with your actual endpoint
        response = self.rest_api_call(url, "get", headers=self.headers)
        print(response)  # Handle the response as needed
    
    # @task
    # def api2(self):
    #     url = "/api/v1/"  # Replace with your actual endpoint
    #     response = self.rest_api_call(url, "get", headers=self.headers)
    #     print(response)

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)
