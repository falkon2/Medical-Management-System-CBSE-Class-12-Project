import streamlit as st
from database import get_db_connection

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
    except Exception as e:
        # Improve error display with emoji
        st.error(f"❌ Registration failed: {e}")
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
