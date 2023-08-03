import requests
from exeptions import (
    UnauthorizedException,
    RegistrationErrorException,
    LogoutErrorException,
    DocumentUploadErrorException,
    GetDocumentsErrorException,
    QueryErrorException,
)
import extra_streamlit_components as stx
import json
import httpx
import logging
import os

BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL")


class HttpClient:
    def __init__(self) -> None:
        self.cookie_manager = stx.CookieManager()
        self.token = None
        self.backend_base_url = BACKEND_BASE_URL + "/api/v1"

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

        if response.status_code != 201:
            raise RegistrationErrorException

        token = response.json()

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
        token = self.get_credentials()
        headers = {
            "Authorization": f"Bearer {token}",
        }
        response = requests.post(
            url,
            headers=headers,
        )

        if response.status_code != 200:
            raise LogoutErrorException("There was a problem with the login")

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

            if response.status_code == 200:
                return {
                    "authentication_status": True,
                    "username": response.json()["email"],
                }

            raise UnauthorizedException("Expired or Incorrect Credentials")

    def upload_document(self, document):
        url = self.backend_base_url + "/documents/upsert-file"
        files = {"file": (document.name, document.read())}
        headers = {
            "Authorization": f"Bearer {self.token}",
        }

        response = httpx.post(url, headers=headers, files=files, timeout=30)

        if response.status_code != 200:
            raise DocumentUploadErrorException

    def get_documents(self):
        headers = {
            "Authorization": f"Bearer {self.token}",
        }

        response = httpx.get(
            self.backend_base_url + "/documents/",
            headers=headers,
        )

        if response.status_code != 200:
            raise GetDocumentsErrorException

        return response.json()["documents"]

    def get_query(self, query, document_id):
        url = self.backend_base_url + "/queries/"
        creds = self.get_credentials()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {creds}",
        }
        payload = {
            "query": query,
            "document_id": document_id,
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload,
        )

        if response.status_code != 200:
            raise QueryErrorException

        data = response.json()
        return data["answer"]

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
