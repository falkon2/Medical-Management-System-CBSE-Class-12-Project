import streamlit as st
from database import init_db
from pages import show_login_page, show_dashboard, show_add_patient, show_view_patients, show_prescriptions

def main():
    # Configure page with improved layout and theme
    st.set_page_config(
        page_title="Doctor's Portal",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'About': "# Doctor's Portal\nA simple medical management system for doctors"
        }
    )
    
    # Add custom styles using markdown
    st.markdown("""
        <style>
        .main {
            padding-top: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize database
    init_db()
    
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    # Show sidebar menu if logged in
    if st.session_state.logged_in:
        # Add logo or icon in sidebar
        st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3774/3774299.png", width=100)
        st.sidebar.title(f"Welcome, Dr. {st.session_state.user['full_name']}")
        
        # Add a divider for visual separation
        st.sidebar.markdown("---")
        
        # Improved menu with icons
        menu = st.sidebar.radio(
            "Menu",
            ["📊 Dashboard", "➕ Add Patient", "👥 View Patients", "💊 Prescriptions"]
        )
        
        # Add some space
        st.sidebar.markdown("---")
        
        # Nicer logout button
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()
        
        # Footer in sidebar
        st.sidebar.markdown("---")
        st.sidebar.caption("© 2023 Doctor's Portal")
        
        # Map the menu items to their functions
        menu_mapping = {
            "📊 Dashboard": show_dashboard,
            "➕ Add Patient": show_add_patient,
            "👥 View Patients": show_view_patients,
            "💊 Prescriptions": show_prescriptions
        }
        
        # Show the selected page
        menu_mapping[menu]()
    else:
        show_login_page()

if __name__ == "__main__":
    main()
