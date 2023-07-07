import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
import extra_streamlit_components as stx
from client import client
from exeptions import UnauthorizedException

st.set_page_config(page_title="QueryX")


@st.cache_data
def init_router():
    return stx.Router({"/login": login, "/signup": signup, "/": app})


# state initialization
if "email" not in st.session_state:
    st.session_state["email"] = None

if "password" not in st.session_state:
    st.session_state["password"] = None

if "token" not in st.session_state:
    st.session_state["token"] = None

if "authentication_status" not in st.session_state:
    st.session_state["authentication_status"] = False

if "history" not in st.session_state:
    st.session_state["history"] = []


def login():
    with st.container():
        email = st.text_input("email", key="login_email")
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
        email = st.text_input("email", key="signup_email")
        password = st.text_input("Password", key="signup_password")
        if st.button("Sign Up"):
            print("----------------------------------------")
            print(email)
            print(password)
            print("----------------------------------------")
            client.register(email=email, password=password)
            # st.session_state.authentication_status = True
            st.write("sending signup request")
            router.route("/")

        if st.button("Already have an account?"):
            router.route("/login")


def app():
    try:
        client.check_status()
    except UnauthorizedException:
        router.route("/login")

    with st.sidebar:
        st.write("My files")
        if st.button("Log out"):
            client.logout()
            router.route("/login")

    uploaded_file = st.file_uploader("Choose a file")

    with st.container():
        query = st.text_input(
            "Query Input", placeholder="Ask", label_visibility="hidden"
        )

        if query != "":
            answer = client.get_query(query=query)
            st.session_state.history.append(answer)
            st.write(f"Answering query: {query}")
            st.write(answer)

        with st.expander("History", expanded=False):
            for response in st.session_state.history:
                st.write(response)


router = init_router()
router.show_route_view()

# if not client.check_status()["authentication_status"] and router.get_url_route() == "/":
#     router.route("/signup")
