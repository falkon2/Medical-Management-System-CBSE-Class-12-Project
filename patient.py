import streamlit as st
from database import get_db_connection

def add_patient(name, age, gender, contact, address, medical_history):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO patients (name, age, gender, contact, address, medical_history) VALUES (%s, %s, %s, %s, %s, %s)",
            (name, age, gender, contact, address, medical_history)
        )
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Failed to add patient: {e}")
        return False
    finally:
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
