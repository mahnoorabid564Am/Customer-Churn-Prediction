import streamlit as st
from dashboard import show_dashboard

if not st.session_state.get("logged_in", False):
    st.warning("Please log in to access this page.")
    st.stop()

show_dashboard()