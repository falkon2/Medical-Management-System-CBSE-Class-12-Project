import streamlit as st
import mysql.connector
from datetime import datetime

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",  # Your MySQL password
        database="medical_system"
    )

# Initialize database and tables
def init_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password"  # Your MySQL password
    )
    cursor = conn.cursor()
    
    # Create database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS medical_system")
    cursor.execute("USE medical_system")
    
    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        full_name VARCHAR(255) NOT NULL,
        email VARCHAR(255),
        specialization VARCHAR(255),
        registration_date DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        age INT,
        gender VARCHAR(10),
        contact VARCHAR(20),
        address TEXT,
        medical_history TEXT,
        registration_date DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prescriptions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        doctor_id INT,
        patient_id INT,
        diagnosis TEXT,
        medicines TEXT,
        notes TEXT,
        prescription_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (doctor_id) REFERENCES doctors(id),
        FOREIGN KEY (patient_id) REFERENCES patients(id)
    )
    """)
    
    conn.commit()
    conn.close()

# User functions
def register_user(username, password, full_name, email, specialization):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO doctors (username, password, full_name, email, specialization) VALUES (%s, %s, %s, %s, %s)",
            (username, password, full_name, email, specialization)
        )
        conn.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Registration failed: {err}")
        return False
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute(
        "SELECT * FROM doctors WHERE username = %s AND password = %s",
        (username, password)
    )
    user = cursor.fetchone()
    conn.close()
    
    return user

# Patient functions
def add_patient(name, age, gender, contact, address, medical_history):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO patients (name, age, gender, contact, address, medical_history) VALUES (%s, %s, %s, %s, %s, %s)",
        (name, age, gender, contact, address, medical_history)
    )
    conn.commit()
    conn.close()

def get_patients():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM patients ORDER BY name")
    patients = cursor.fetchall()
    conn.close()
    
    return patients

def get_patient(patient_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
    patient = cursor.fetchone()
    conn.close()
    
    return patient

# Prescription functions
def add_prescription(doctor_id, patient_id, diagnosis, medicines, notes):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO prescriptions (doctor_id, patient_id, diagnosis, medicines, notes) VALUES (%s, %s, %s, %s, %s)",
        (doctor_id, patient_id, diagnosis, medicines, notes)
    )
    conn.commit()
    conn.close()

def get_patient_prescriptions(patient_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT p.*, d.full_name as doctor_name 
        FROM prescriptions p
        JOIN doctors d ON p.doctor_id = d.id
        WHERE p.patient_id = %s
        ORDER BY p.prescription_date DESC
    """, (patient_id,))
    
    prescriptions = cursor.fetchall()
    conn.close()
    
    return prescriptions

# Main app
def main():
    st.set_page_config(page_title="Doctor's Portal", layout="wide")
    
    # Set up database
    init_db()
    
    # Session state init
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    # Sidebar menu
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
    
    # Main content
    if not st.session_state.logged_in:
        login_register_page()
    else:
        if menu == "Dashboard":
            dashboard_page()
        elif menu == "Add Patient":
            add_patient_page()
        elif menu == "View Patients":
            view_patients_page()
        elif menu == "Prescriptions":
            prescriptions_page()

# Pages
def login_register_page():
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

def dashboard_page():
    st.title("Dashboard")
    
    # Get stats
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM patients")
    patient_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM prescriptions WHERE doctor_id = %s", 
                  (st.session_state.user['id'],))
    prescription_count = cursor.fetchone()[0]
    
    # Recent prescriptions
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.prescription_date, pt.name as patient_name, p.diagnosis 
        FROM prescriptions p
        JOIN patients pt ON p.patient_id = pt.id
        WHERE p.doctor_id = %s
        ORDER BY p.prescription_date DESC
        LIMIT 5
    """, (st.session_state.user['id'],))
    
    recent_prescriptions = cursor.fetchall()
    conn.close()
    
    # Display stats
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Patients", patient_count)
    with col2:
        st.metric("Your Prescriptions", prescription_count)
    
    # Recent activity
    st.subheader("Recent Prescriptions")
    if recent_prescriptions:
        for rx in recent_prescriptions:
            st.write(f"{rx['prescription_date']}: {rx['patient_name']} - {rx['diagnosis']}")
    else:
        st.write("No recent prescriptions")

def add_patient_page():
    st.title("Add New Patient")
    
    name = st.text_input("Patient Name")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    contact = st.text_input("Contact Number")
    address = st.text_area("Address")
    medical_history = st.text_area("Medical History")
    
    if st.button("Add Patient"):
        if name:
            add_patient(name, age, gender, contact, address, medical_history)
            st.success(f"Patient {name} added successfully!")
            st.rerun()
        else:
            st.warning("Patient name is required")

def view_patients_page():
    st.title("View Patients")
    
    patients = get_patients()
    
    if not patients:
        st.info("No patients found.")
        return
    
    # Search box
    search_term = st.text_input("Search patients by name")
    
    filtered_patients = patients
    if search_term:
        filtered_patients = [p for p in patients if search_term.lower() in p['name'].lower()]
    
    # Show patients
    for patient in filtered_patients:
        with st.expander(f"{patient['name']} (Age: {patient['age']})"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Gender:** {patient['gender']}")
                st.write(f"**Contact:** {patient['contact']}")
                st.write(f"**Address:** {patient['address']}")
                
            with col2:
                st.write(f"**Medical History:** {patient['medical_history']}")
                st.write(f"**Registered on:** {patient['registration_date']}")
            
            # Buttons
            if st.button("View Prescriptions", key=f"view_{patient['id']}"):
                st.session_state.selected_patient = patient
                st.session_state.view_prescriptions = True
                st.rerun()
                
            if st.button("Add Prescription", key=f"add_{patient['id']}"):
                st.session_state.selected_patient = patient
                st.session_state.add_prescription = True
                st.rerun()
    
    # Handle viewing prescriptions
    if 'view_prescriptions' in st.session_state and st.session_state.view_prescriptions:
        view_patient_prescriptions(st.session_state.selected_patient)
        st.session_state.view_prescriptions = False
        
    # Handle adding prescriptions
    if 'add_prescription' in st.session_state and st.session_state.add_prescription:
        add_prescription_form(st.session_state.selected_patient)
        st.session_state.add_prescription = False

def view_patient_prescriptions(patient):
    st.subheader(f"Prescriptions for {patient['name']}")
    
    prescriptions = get_patient_prescriptions(patient['id'])
    
    if not prescriptions:
        st.info(f"No prescriptions found for {patient['name']}")
        return
    
    for rx in prescriptions:
        with st.expander(f"Prescription from {rx['prescription_date']}"):
            st.write(f"**Doctor:** {rx['doctor_name']}")
            st.write(f"**Diagnosis:** {rx['diagnosis']}")
            st.write(f"**Medicines:**")
            st.code(rx['medicines'])
            st.write(f"**Notes:** {rx['notes']}")

def add_prescription_form(patient):
    st.subheader(f"Add Prescription for {patient['name']}")
    
    diagnosis = st.text_area("Diagnosis")
    medicines = st.text_area("Medicines (one per line)")
    notes = st.text_area("Additional Notes")
    
    if st.button("Save Prescription"):
        if diagnosis and medicines:
            doctor_id = st.session_state.user['id']
            patient_id = patient['id']
            add_prescription(doctor_id, patient_id, diagnosis, medicines, notes)
            st.success("Prescription added successfully!")
        else:
            st.warning("Diagnosis and medicines are required")

def prescriptions_page():
    st.title("Prescriptions")
    
    # Get patients for the dropdown
    patients = get_patients()
    
    if not patients:
        st.info("No patients in the system. Add patients first.")
        return
    
    # Selection box
    patient_names = [f"{p['name']} (ID: {p['id']})" for p in patients]
    selected_patient = st.selectbox("Select a patient", patient_names)
    
    if selected_patient:
        # Get patient ID
        patient_id = int(selected_patient.split("ID: ")[1].strip(")"))
        patient = get_patient(patient_id)
        
        # Tabs
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
                    add_prescription(doctor_id, patient_id, diagnosis, medicines, notes)
                    st.success("Prescription added successfully!")
                    st.rerun()
                else:
                    st.warning("Diagnosis and medicines are required")

if __name__ == "__main__":
    main()
