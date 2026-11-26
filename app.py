import streamlit as st
from auth import login_user,register_user
#making the seesion condition
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None 
# on login this condition becomes true and user is moved to main page
if st.session_state["logged_in"]:
    st.title("Dashboard")  
    st.title("Welcome to Customer Churn Analytics")

    st.write(
    "Use the sidebar to explore customer data, "
    "analyze churn patterns, and demonstrate churn risk."
             )
    
    logout_button = st.button("Logout")
    if logout_button:
        st.session_state["logged_in"]=False
        st.session_state["user_id"]=None  
        st.rerun() 
# if user is logged out he'll be moved to login or registration page
else:
    st.title("Customer Churn Prediction")
    choice = st.radio("Select an option", ["Login", "Sign Up"])
    if choice =="Login":
        st.subheader("Login")
        email = st.text_input("Enter your email")    
        password = st.text_input("Enter your password" ,type="password")
        login_button=st.button("Login")
        if login_button:
            user_id=login_user(email,password)
            if user_id:
                st.session_state["logged_in"]=True
                st.session_state["user_id"]=user_id
                st.success("sucessful login")
                st.rerun()
            else:
                st.error("Invalid email or password.")  
    else:
        st.subheader("Registration Form")
        reg_name=st.text_input("Enter your name: ")
        reg_email=st.text_input("Enter your Email: ")
        reg_pass=st.text_input("Enter your password: ",type="password")
        reg_button = st.button("Create Account")
        if reg_button:
            result = register_user(reg_name,reg_email,reg_pass)
            if result:
                st.success("Account created successfully!")
            else:
             st.error("Email already registered!")