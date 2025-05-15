import mysql.connector
from config import DB_CONFIG
import streamlit as st

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def init_db():
    # Connect to MySQL without database specified
    conn = mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"]
    )
    cursor = conn.cursor()
    
    # Create database and tables
    cursor.execute("CREATE DATABASE IF NOT EXISTS medical_system")
    cursor.execute("USE medical_system")
    
    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) NOT NULL,
        password VARCHAR(255) NOT NULL,
        full_name VARCHAR(255) NOT NULL,
        email VARCHAR(255),
        specialization VARCHAR(255)
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
        medical_history TEXT
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
        prescription_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (doctor_id) REFERENCES doctors(id),
        FOREIGN KEY (patient_id) REFERENCES patients(id)
    )
    """)
    
    # Create simple indexes
    try:
        cursor.execute("CREATE INDEX idx_doctor_username ON doctors(username)")
    except:
        pass  # Index might already exist
        
    try:
        cursor.execute("CREATE INDEX idx_patient_name ON patients(name)")
    except:
        pass  # Index might already exist
    
    conn.commit()
    conn.close()
