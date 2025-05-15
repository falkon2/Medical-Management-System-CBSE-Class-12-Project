import streamlit as st
from database import init_db
from pages import show_login_page, show_dashboard, show_add_patient, show_view_patients, show_prescriptions

def main():
    st.set_page_config(page_title="Doctor's Portal", layout="wide")
    
    # Initialize database
    init_db()
    
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    # Show sidebar menu if logged in
    if st.session_state.logged_in:
        st.sidebar.title(f"Welcome, Dr. {st.session_state.user['full_name']}")
        menu = st.sidebar.radio(
            "Menu",
            ["Dashboard", "Add Patient", "View Patients", "Prescriptions"]
        )
        
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()
        
        # Show selected page
        if menu == "Dashboard":
            show_dashboard()
        elif menu == "Add Patient":
            show_add_patient()
        elif menu == "View Patients":
            show_view_patients()
        elif menu == "Prescriptions":
            show_prescriptions()
    else:
        show_login_page()

if __name__ == "__main__":
    main()
