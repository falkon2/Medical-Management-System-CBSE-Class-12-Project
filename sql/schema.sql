-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS medical_system;
USE medical_system;

-- Create doctors table
CREATE TABLE IF NOT EXISTS doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    specialization VARCHAR(255),
    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create patients table
CREATE TABLE IF NOT EXISTS patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT,
    gender VARCHAR(10),
    contact VARCHAR(20),
    address TEXT,
    medical_history TEXT,
    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create prescriptions table
CREATE TABLE IF NOT EXISTS prescriptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    doctor_id INT,
    patient_id INT,
    diagnosis TEXT,
    medicines TEXT,
    notes TEXT,
    prescription_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
);

-- Insert sample doctor data (using plain text password)
INSERT INTO doctors (username, password, full_name, email, specialization)
VALUES
('admin', 'admin123', 'Admin Doctor', 'admin@example.com', 'General Medicine')
ON DUPLICATE KEY UPDATE
    password = VALUES(password),
    full_name = VALUES(full_name),
    email = VALUES(email),
    specialization = VALUES(specialization);

-- Insert sample patient data
INSERT INTO patients (name, age, gender, contact, address, medical_history)
VALUES
('John Doe', 45, 'Male', '9876543210', '123 Main St, City', 'Hypertension, Diabetes'),
('Jane Smith', 35, 'Female', '8765432109', '456 Park Ave, Town', 'Asthma')
ON DUPLICATE KEY UPDATE
    name = VALUES(name);

-- Create indexes for better performance
CREATE INDEX idx_doctor_username ON doctors(username);
CREATE INDEX idx_patient_name ON patients(name);
CREATE INDEX idx_prescription_doctor ON prescriptions(doctor_id);
CREATE INDEX idx_prescription_patient ON prescriptions(patient_id);
