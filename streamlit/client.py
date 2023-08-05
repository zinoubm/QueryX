import requests
from exeptions import (
    UnauthorizedException,
    RegistrationErrorException,
    LogoutErrorException,
    DocumentUploadErrorException,
    GetDocumentsErrorException,
    QueryErrorException,
)
import streamlit as st
import extra_streamlit_components as stx
import json
from datetime import datetime, timedelta
import httpx
import logging
import os
from time import sleep

BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL")


class HttpClient:
    def __init__(self, session_state) -> None:
        self.cookie_manager = stx.CookieManager()
        inited = False
        while not inited:
            try:
                inited = self.cookie_manager.get_all()
            except st.errors.DuplicateWidgetID:
                pass
            if not inited:
                sleep(0.02)

        self.session_state = session_state
        self.session = requests.Session()
        self.backend_base_url = BACKEND_BASE_URL + "/api/v1"

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
            logging.warning("not token")
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
            logging.warning("expired token")
            raise UnauthorizedException("Expired or Incorrect Credentials")

    def upload_document(self, document):
        url = self.backend_base_url + "/documents/upsert-file"
        files = {"file": (document.name, document.read())}
        creds = self.get_credentials()
        headers = {
            "Authorization": f"Bearer {creds}",
        }

        response = httpx.post(url, headers=headers, files=files, timeout=30)

        if response.status_code != 200:
            raise DocumentUploadErrorException

    def get_documents(self):
        creds = self.get_credentials()
        headers = {
            "Authorization": f"Bearer {creds}",
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

    # store creds using session_state
    # def set_credentials(self, creds):
    #     self.session_state["token"] = creds

    # def get_credentials(self):
    #     return self.session_state["token"]

    # def delete_credentials(self):
    #     self.session_state["token"] = None

    # store creds using requests
    # def set_credentials(self, creds):
    #     self.session.cookies.set("token", creds)

    # def get_credentials(self):
    #     return self.session.cookies.get("token")

    # def delete_credentials(self):
    #     self.session.cookies.clear()

    # store creds using browser cookies
    def set_credentials(self, creds):
        self.cookie_manager.set(
            "jwt_token", creds, expires_at=datetime.utcnow() + timedelta(days=7)
        )

    def get_credentials(self):
        return self.cookie_manager.get(cookie="jwt_token")

    def delete_credentials(self):
        self.cookie_manager.delete(cookie="jwt_token")


# client = HttpClient()
