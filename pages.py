import streamlit as st
from user import authenticate_user, register_user
from patient import add_patient, get_patients, get_patient
from prescription import add_prescription, get_patient_prescriptions, get_doctor_stats

def show_login_page():
    st.title("Doctor's Portal")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.header("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            if username and password:
                user = authenticate_user(username, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Wrong username or password")
            else:
                st.warning("Please enter username and password")
    
    with tab2:
        st.header("Register")
        new_username = st.text_input("Username", key="reg_username")
        new_password = st.text_input("Password", type="password", key="reg_password")
        confirm_password = st.text_input("Confirm Password", type="password")
        full_name = st.text_input("Full Name")
        email = st.text_input("Email")
        specialization = st.text_input("Specialization")
        
        if st.button("Register"):
            if new_password != confirm_password:
                st.error("Passwords don't match")
            elif not (new_username and new_password and full_name):
                st.warning("Username, password and name are required")
            else:
                if register_user(new_username, new_password, full_name, email, specialization):
                    st.success("Registration successful! You can now login.")
                    st.rerun()

def show_dashboard():
    st.title("Dashboard")
    
    stats = get_doctor_stats(st.session_state.user['id'])
    
    # Display stats
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Patients", stats["patient_count"])
    with col2:
        st.metric("Your Prescriptions", stats["prescription_count"])
    
    # Display recent activity
    st.subheader("Recent Prescriptions")
    if stats["recent_prescriptions"]:
        for rx in stats["recent_prescriptions"]:
            st.write(f"{rx['prescription_date']}: {rx['patient_name']} - {rx['diagnosis']}")
    else:
        st.write("No recent prescriptions")

def show_add_patient():
    st.title("Add New Patient")
    
    name = st.text_input("Patient Name")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    contact = st.text_input("Contact Number")
    address = st.text_area("Address")
    medical_history = st.text_area("Medical History")
    
    if st.button("Add Patient"):
        if name:
            if add_patient(name, age, gender, contact, address, medical_history):
                st.success(f"Patient {name} added successfully!")
                st.rerun()
        else:
            st.warning("Patient name is required")

def show_view_patients():
    st.title("View Patients")
    
    patients = get_patients()
    
    if not patients:
        st.info("No patients found.")
        return
    
    # Search functionality
    search = st.text_input("Search patients by name")
    
    filtered_patients = patients
    if search:
        filtered_patients = [p for p in patients if search.lower() in p['name'].lower()]
    
    for patient in filtered_patients:
        with st.expander(f"{patient['name']} (Age: {patient.get('age', 'N/A')})"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Gender:** {patient.get('gender', 'N/A')}")
                st.write(f"**Contact:** {patient.get('contact', 'N/A')}")
                st.write(f"**Address:** {patient.get('address', 'N/A')}")
            
            with col2:
                st.write(f"**Medical History:** {patient.get('medical_history', 'N/A')}")
            
            # View/Add prescription buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("View Prescriptions", key=f"view_{patient['id']}"):
                    st.session_state.view_patient = patient
                    st.rerun()
            with col2:
                if st.button("Add Prescription", key=f"add_{patient['id']}"):
                    st.session_state.add_prescription_patient = patient
                    st.rerun()
    
    # Handle viewing prescriptions
    if 'view_patient' in st.session_state:
        patient = st.session_state.view_patient
        st.subheader(f"Prescriptions for {patient['name']}")
        
        prescriptions = get_patient_prescriptions(patient['id'])
        
        if not prescriptions:
            st.info(f"No prescriptions found for {patient['name']}")
        else:
            for rx in prescriptions:
                with st.expander(f"Prescription from {rx['prescription_date']}"):
                    st.write(f"**Doctor:** {rx['doctor_name']}")
                    st.write(f"**Diagnosis:** {rx['diagnosis']}")
                    st.write(f"**Medicines:**")
                    st.code(rx['medicines'])
                    st.write(f"**Notes:** {rx['notes']}")
        
        if st.button("Close"):
            del st.session_state.view_patient
            st.rerun()
    
    # Handle adding prescriptions
    if 'add_prescription_patient' in st.session_state:
        patient = st.session_state.add_prescription_patient
        st.subheader(f"Add Prescription for {patient['name']}")
        
        diagnosis = st.text_area("Diagnosis")
        medicines = st.text_area("Medicines (one per line)")
        notes = st.text_area("Additional Notes")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Save Prescription"):
                if diagnosis and medicines:
                    if add_prescription(st.session_state.user['id'], patient['id'], diagnosis, medicines, notes):
                        st.success("Prescription added successfully!")
                        del st.session_state.add_prescription_patient
                        st.rerun()
                else:
                    st.warning("Diagnosis and medicines are required")
        with col2:
            if st.button("Cancel"):
                del st.session_state.add_prescription_patient
                st.rerun()

def show_prescriptions():
    st.title("Prescriptions")
    
    # Get all patients for the dropdown
    patients = get_patients()
    
    if not patients:
        st.info("No patients in the system. Add patients first.")
        return
    
    # Create a selection box for patients
    patient_names = [f"{p['name']} (ID: {p['id']})" for p in patients]
    selected_patient = st.selectbox("Select a patient", patient_names)
    
    if selected_patient:
        # Extract patient ID from selection
        patient_id = int(selected_patient.split("ID: ")[1].strip(")"))
        patient = get_patient(patient_id)
        
        # Tab for viewing or adding prescriptions
        tab1, tab2 = st.tabs(["View Prescriptions", "Add New Prescription"])
        
        with tab1:
            prescriptions = get_patient_prescriptions(patient_id)
            if prescriptions:
                for rx in prescriptions:
                    with st.expander(f"Prescription from {rx['prescription_date']}"):
                        st.write(f"**Doctor:** {rx['doctor_name']}")
                        st.write(f"**Diagnosis:** {rx['diagnosis']}")
                        st.write(f"**Medicines:**")
                        st.code(rx['medicines'])
                        st.write(f"**Notes:** {rx['notes']}")
            else:
                st.info(f"No prescriptions found for {patient['name']}")
        
        with tab2:
            diagnosis = st.text_area("Diagnosis")
            medicines = st.text_area("Medicines (one per line)")
            notes = st.text_area("Additional Notes")
            
            if st.button("Save Prescription"):
                if diagnosis and medicines:
                    doctor_id = st.session_state.user['id']
                    if add_prescription(doctor_id, patient_id, diagnosis, medicines, notes):
                        st.success("Prescription added successfully!")
                        st.rerun()
                else:
                    st.warning("Diagnosis and medicines are required")
