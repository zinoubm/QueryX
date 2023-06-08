# import extra_streamlit_components as stx
import requests
from datetime import datetime, timedelta
from exeptions import UnauthorizedException
import extra_streamlit_components as stx
import json


class HttpClient:
    def __init__(self) -> None:
        self.cookie_manager = stx.CookieManager()
        self.token = None
        self.backend_base_url = "http://backend:8000/api/v1"

    def request(func):
        def inner(self):
            self.check_status()
            func(self)

        return inner

    def register(self, email: str, password: str):
        url = self.backend_base_url + "/auth/register"

        payload = {"email": email, "password": password}

        headers = {"Content-Type": "application/json"}

        response = requests.post(url, data=json.dumps(payload), headers=headers)

        token = response.json()

        print(token)
        print("status")
        print(response.status_code)

    def login(self, username, password):
        url = self.backend_base_url + "/auth/jwt/login"
        data = {"username": username, "password": password}

        response = requests.post(
            url,
            data=data,
        )

        if response.status_code != 200:
            raise UnauthorizedException("There was a problem with the login")

        token = response.json()["access_token"]

        self.set_credentials(token)

    @request
    def logout(self):
        url = self.backend_base_url + "/auth/jwt/logout"

        print("bearer token")
        token = self.get_credentials()
        print(token)

        headers = {
            "Authorization": f"Bearer {token}",
        }

        response = requests.post(
            url,
            headers=headers,
        )

        self.delete_credentials()

    def check_status(self):
        creds = self.get_credentials()

        if creds is None:
            raise UnauthorizedException("No Credentails")

        if creds:
            url = self.backend_base_url + "/users/me"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {creds}",
            }

            response = requests.get(url, headers=headers)
            response_content = response.json()

            if response.status_code == 200:
                return {
                    "authentication_status": True,
                    "username": response_content["email"],
                }

            raise UnauthorizedException("Expired or Incorrect Credentials")

    def get_query(self, query):
        # self.check_status()
        url = self.backend_base_url + "/queries/" + query
        creds = self.get_credentials()

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {creds}",
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data["answer"]

        raise UnauthorizedException

    def set_credentials(self, creds):
        self.token = creds

    def get_credentials(self):
        return self.token

    def delete_credentials(self):
        self.token = None

    # def set_credentials(self, creds):
    #     self.cookie_manager.set(
    #         "jwt_token", creds, expires_at=datetime.utcnow() + timedelta(days=7)
    #     )

    # def get_credentials(self):
    #     temp = self.cookie_manager.get(cookie="jwt_token")
    #     return temp

    # def delete_credentials(self):
    #     self.cookie_manager.delete(cookie="jwt_token")


client = HttpClient()

if __name__ == "__main__":
    email = "zanzan.arthur@camelot.bt"
    password = "gui23nevere"

    # client = HttpClient()
    # client.register(email, password)

    # login
    try:
        client.login(username=email, password=password)

    except UnauthorizedException as e:
        print("route to login")

    # get_credentials
    # print("credentials from client")
    # print(client.get_credentials())

    # check_status
    print("checking the status")
    try:
        client.check_status()

    except UnauthorizedException as e:
        print("route to login")

    client.get_query("What is twitter")

    # logout
    client.logout()
