import streamlit as st
from database import get_db_connection

def add_prescription(doctor_id, patient_id, diagnosis, medicines, notes):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO prescriptions (doctor_id, patient_id, diagnosis, medicines, notes) VALUES (%s, %s, %s, %s, %s)",
            (doctor_id, patient_id, diagnosis, medicines, notes)
        )
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Failed to add prescription: {e}")
        return False
    finally:
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

def get_doctor_stats(doctor_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Count total patients
    cursor.execute("SELECT COUNT(*) FROM patients")
    patient_count = cursor.fetchone()[0]
    
    # Count prescriptions by this doctor
    cursor.execute("SELECT COUNT(*) FROM prescriptions WHERE doctor_id = %s", (doctor_id,))
    prescription_count = cursor.fetchone()[0]
    
    # Get recent prescriptions
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.prescription_date, pt.name as patient_name, p.diagnosis 
        FROM prescriptions p
        JOIN patients pt ON p.patient_id = pt.id
        WHERE p.doctor_id = %s
        ORDER BY p.prescription_date DESC
        LIMIT 5
    """, (doctor_id,))
    
    recent_prescriptions = cursor.fetchall()
    conn.close()
    
    return {
        "patient_count": patient_count,
        "prescription_count": prescription_count,
        "recent_prescriptions": recent_prescriptions
    }
