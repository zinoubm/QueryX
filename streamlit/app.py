import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
import extra_streamlit_components as stx
from client import HttpClient
from exeptions import (
    UnauthorizedException,
    RegistrationErrorException,
    LogoutErrorException,
    DocumentUploadErrorException,
    GetDocumentsErrorException,
    QueryErrorException,
)

try:
    st.set_page_config(page_title="OpenPdf")
except Exception as e:
    print("Initializing The Client!")


@st.cache_data
def init_router():
    return stx.Router({"/login": login, "/signup": signup, "/": app})


if "username" not in st.session_state:
    st.session_state["username"] = None
if "history" not in st.session_state:
    st.session_state["history"] = []
if "document_id" not in st.session_state:
    st.session_state["document_id"] = None
if "token" not in st.session_state:
    st.session_state["token"] = None
if "documents_names" not in st.session_state:
    st.session_state["documents_names"] = None
if "names_to_ids" not in st.session_state:
    st.session_state["names_to_ids"] = None


client = HttpClient(st.session_state)


def login():
    with st.container():
        st.title("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", key="login_password")
        if st.button("Login"):
            try:
                client.login(username=email, password=password)
                st.write(f"Sending login request")
                router.route("/")
            except UnauthorizedException:
                st.warning("Wrong Inputs")

        if st.button("Don't have an account?"):
            router.route("/signup")


def signup():
    with st.container():
        st.title("Signup")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", key="signup_password")
        if st.button("Sign Up"):
            try:
                client.register(email=email, password=password)
                st.write("sending signup request")
                router.route("/")
            except RegistrationErrorException:
                st.warning("Couldn't Register, Please Try Again!")

        if st.button("Already have an account?"):
            router.route("/login")


def update_documents():
    documents = client.get_documents()
    documents_names = [document["name"] for document in documents]
    names_to_ids = {document["name"]: document["id"] for document in documents}
    st.session_state["documents_names"] = documents_names
    st.session_state["names_to_ids"] = names_to_ids


def app():
    try:
        user = client.check_status()
        st.session_state["username"] = user["username"]
    except UnauthorizedException:
        router.route("/login")
        st.warning("Your Sessiong Expired, Please LogIn!")

    with st.sidebar:
        st.title("OpenPdf")
        st.write("Hi " + st.session_state["username"])
        try:
            update_documents()
            option = st.selectbox(
                "Please, Select a Document.",
                st.session_state["documents_names"],
            )

        except GetDocumentsErrorException:
            option = None
            st.warning("Couldn't Get Documents, Please Refresh And Try Again!")

        if option:
            st.session_state["document_id"] = st.session_state["names_to_ids"][option]

        if st.button("Log out"):
            try:
                client.logout()
            except LogoutErrorException:
                router.route("/login")

    uploaded_file = st.file_uploader("Choose a file")
    if st.button("Upload") and uploaded_file:
        try:
            client.upload_document(uploaded_file)
            st.info("Document Uploaded Successfuly :)")
            update_documents()
        except DocumentUploadErrorException:
            st.warning("Couldn't Upload Document, Please Refresh And Try Again!")

    with st.container():
        query = st.text_input(
            "Query Input", placeholder="Ask", label_visibility="hidden"
        )

        if query != "" and st.session_state["document_id"] is not None:
            try:
                answer = client.get_query(
                    query=query, document_id=st.session_state["document_id"]
                )

                st.session_state.history.append(answer)
                st.write(f"Answering query: {query}")
                st.write(answer)
            except QueryErrorException:
                st.warning("Couldn't Get Answer, Please Refresh And Try Again!")

        with st.expander("History", expanded=False):
            for response in st.session_state.history:
                st.write(response)


router = init_router()

router.show_route_view()
