# Medical Management System - CBSE Class 12 Project

This is a simple medical management system created for CBSE Class 12 project using Streamlit and MySQL.

## Project Features

- Doctor registration and login
- Patient management
  - Add new patients
  - View existing patients
  - Search for patients
- Prescription management
  - Create prescriptions for patients
  - View prescription history
- Doctor dashboard with statistics

## Setup Instructions

1. Make sure you have Python and MySQL installed
2. Create a MySQL database (or it will be created automatically when running the app)
3. Install the required packages using:
   ```
   pip install -r requirements.txt
   ```
4. Update the database connection settings in app.py if needed
5. Run the application:
   ```
   streamlit run app.py
   ```

## How to Use

1. Register as a doctor or login with existing credentials
2. Navigate using the sidebar menu:
   - Dashboard: View statistics and recent activity
   - Add Patient: Register new patients
   - View Patients: See all patients and their details
   - Prescriptions: Manage patient prescriptions

## Database Structure

The application uses three main tables:
- doctors: Stores doctor credentials and information
- patients: Stores patient details
- prescriptions: Records prescriptions created by doctors for patients