import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
import os
import json
import base64
import io
from PIL import Image, ImageDraw
import random

# Page configuration
st.set_page_config(
    page_title="Event Check Attendance System",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
def apply_custom_css():
    st.markdown("""
    <style>
    /* Main styling */
    .main-header {
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .stat-card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
        margin-bottom: 15px;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1e3c72;
        margin: 10px 0;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #666;
    }
    
    .feature-card {
        background-color: white;
        border-radius: 10px;
        padding: 25px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        margin-bottom: 20px;
        height: 100%;
    }
    
    .feature-title {
        font-size: 1.3rem;
        color: #1e3c72;
        margin-bottom: 15px;
    }
    
    .feature-description {
        color: #666;
        margin-bottom: 20px;
        line-height: 1.5;
    }
    
    .security-section {
        background-color: white;
        border-radius: 10px;
        padding: 25px;
        margin-top: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    
    .security-title {
        font-size: 1.5rem;
        color: #1e3c72;
        margin-bottom: 20px;
        text-align: center;
    }
    
    .security-item {
        text-align: center;
        padding: 15px;
    }
    
    .security-icon {
        font-size: 2.5rem;
        margin-bottom: 15px;
        color: #1e3c72;
    }
    
    .security-label {
        font-weight: 600;
        margin-bottom: 10px;
        color: #333;
    }
    
    .security-description {
        color: #666;
        font-size: 0.9rem;
    }
    
    .btn {
        display: inline-block;
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        color: white;
        padding: 12px 25px;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        text-decoration: none;
        text-align: center;
        width: 100%;
        margin-bottom: 10px;
    }
    
    .btn:hover {
        background: linear-gradient(135deg, #2a5298, #3a62a8);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    .btn-success {
        background: linear-gradient(135deg, #27ae60, #2ecc71);
    }
    
    .btn-success:hover {
        background: linear-gradient(135deg, #2ecc71, #27ae60);
    }
    
    .btn-warning {
        background: linear-gradient(135deg, #f39c12, #e67e22);
    }
    
    .btn-warning:hover {
        background: linear-gradient(135deg, #e67e22, #f39c12);
    }
    
    .btn-logout {
        background: linear-gradient(135deg, #e74c3c, #c0392b);
    }
    
    .btn-logout:hover {
        background: linear-gradient(135deg, #c0392b, #a93226);
    }
    
    .user-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #1e3c72;
        font-weight: bold;
        margin-right: 10px;
    }
    
    .user-controls {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        margin-bottom: 20px;
    }
    
    .scanner-container {
        border: 2px dashed #1e3c72;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        margin: 20px 0;
        background-color: #f0f4ff;
    }
    
    .scan-result {
        margin-top: 20px;
        padding: 15px;
        border-radius: 8px;
        background-color: #e8f6ef;
        border: 1px solid #27ae60;
        text-align: center;
    }
    
    .scan-result.error {
        background-color: #fdeaea;
        border-color: #e74c3c;
        color: #e74c3c;
    }
    
    .attendance-item {
        padding: 12px 15px;
        border-bottom: 1px solid #eee;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .attendance-item:last-child {
        border-bottom: none;
    }
    
    .attendance-name {
        font-weight: 600;
    }
    
    .attendance-time {
        color: #666;
        font-size: 0.9rem;
    }
    
    .status-badge {
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .status-present {
        background-color: #e8f6ef;
        color: #27ae60;
    }
    
    .status-absent {
        background-color: #fdeaea;
        color: #e74c3c;
    }
    
    .student-info {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        border-left: 4px solid #1e3c72;
    }
    
    .student-details {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
    }
    
    .student-detail {
        display: flex;
        flex-direction: column;
    }
    
    .student-label {
        font-weight: 600;
        color: #1e3c72;
        font-size: 0.9rem;
    }
    
    .student-value {
        font-size: 1rem;
    }
    
    /* QR Code Canvas */
    .qr-code-canvas {
        border: 1px solid #ddd;
        background: white;
        margin: 20px auto;
        display: block;
    }
    
    /* Signature Canvas */
    .signature-pad {
        border: 1px solid #ddd;
        border-radius: 5px;
        margin: 15px 0;
        background-color: #f9f9f9;
        cursor: crosshair;
    }
    
    /* Fingerprint Scanner */
    .fingerprint-scanner {
        width: 200px;
        height: 200px;
        margin: 20px auto;
        border: 2px dashed #1e3c72;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #f0f4ff;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .fingerprint-scanner.scanning {
        border-color: #27ae60;
        background-color: #e8f6ef;
    }
    
    .scanner-animation {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        background: radial-gradient(circle, #1e3c72 0%, #2a5298 100%);
        display: flex;
        justify-content: center;
        align-items: center;
        color: white;
        font-weight: bold;
        transition: all 0.5s ease;
    }
    
    .scanner-animation.scanning {
        background: radial-gradient(circle, #27ae60 0%, #2ecc71 100%);
    }
    </style>
    """, unsafe_allow_html=True)

class AttendanceSystem:
    def __init__(self):
        self.attendance_file = "attendance_data.csv"
        self.students_file = "students_data.json"
        self.load_data()
    
    def load_data(self):
        """Load data from files"""
        try:
            # Load attendance data
            if os.path.exists(self.attendance_file):
                self.attendance_df = pd.read_csv(self.attendance_file)
                # Ensure all required columns exist
                required_columns = ['StudentID', 'Name', 'Date', 'Time', 'Method', 'Status']
                for col in required_columns:
                    if col not in self.attendance_df.columns:
                        self.attendance_df[col] = ""
            else:
                self.attendance_df = pd.DataFrame(columns=[
                    'StudentID', 'Name', 'Date', 'Time', 'Method', 'Status'
                ])
            
            # Load students data
            if os.path.exists(self.students_file):
                with open(self.students_file, 'r') as f:
                    self.students_data = json.load(f)
            else:
                self.students_data = {}
                
        except Exception as e:
            st.error(f"Error loading data: {e}")
            self.attendance_df = pd.DataFrame(columns=[
                'StudentID', 'Name', 'Date', 'Time', 'Method', 'Status'
            ])
            self.students_data = {}
    
    def save_data(self):
        """Save data to files"""
        try:
            self.attendance_df.to_csv(self.attendance_file, index=False)
            with open(self.students_file, 'w') as f:
                json.dump(self.students_data, f, indent=4)
        except Exception as e:
            st.error(f"Error saving data: {e}")
    
    def mark_attendance(self, student_id, name, method="Manual"):
        """Mark attendance for a student"""
        try:
            current_time = datetime.now()
            today_date = current_time.date()
            current_time_str = current_time.strftime("%H:%M:%S")
            
            # Check if already marked today
            if not self.attendance_df.empty and 'Date' in self.attendance_df.columns:
                existing_record = self.attendance_df[
                    (self.attendance_df['StudentID'].astype(str) == str(student_id)) & 
                    (self.attendance_df['Date'] == str(today_date))
                ]
                
                if not existing_record.empty:
                    return False, "⚠️ Attendance already marked today"
            
            # Add new record
            new_record = {
                'StudentID': str(student_id),
                'Name': name,
                'Date': str(today_date),
                'Time': current_time_str,
                'Method': method,
                'Status': 'Present'
            }
            
            new_df = pd.DataFrame([new_record])
            self.attendance_df = pd.concat([self.attendance_df, new_df], ignore_index=True)
            self.save_data()
            return True, "✅ Attendance marked successfully!"
            
        except Exception as e:
            return False, f"❌ Error: {str(e)}"
    
    def add_student(self, student_id, name, department="General"):
        """Add a new student"""
        try:
            self.students_data[str(student_id)] = {
                'name': name,
                'department': department,
                'added_date': str(date.today())
            }
            self.save_data()
            return True, "✅ Student added successfully!"
        except Exception as e:
            return False, f"❌ Error: {str(e)}"
    
    def get_today_attendance(self):
        """Get today's attendance records"""
        today = str(date.today())
        if not self.attendance_df.empty and 'Date' in self.attendance_df.columns:
            return self.attendance_df[self.attendance_df['Date'] == today]
        else:
            return pd.DataFrame()
    
    def get_student_attendance(self, student_id):
        """Get attendance records for specific student"""
        if not self.attendance_df.empty:
            return self.attendance_df[
                self.attendance_df['StudentID'].astype(str) == str(student_id)
            ]
        else:
            return pd.DataFrame()
    
    def delete_student(self, student_id):
        """Delete a student"""
        try:
            if student_id in self.students_data:
                del self.students_data[student_id]
                self.save_data()
                return True, "✅ Student deleted successfully!"
            else:
                return False, "❌ Student not found!"
        except Exception as e:
            return False, f"❌ Error: {str(e)}"
    
    def clear_today_attendance(self):
        """Clear today's attendance records"""
        try:
            today = str(date.today())
            if not self.attendance_df.empty:
                initial_count = len(self.attendance_df)
                self.attendance_df = self.attendance_df[self.attendance_df['Date'] != today]
                final_count = len(self.attendance_df)
                deleted_count = initial_count - final_count
                self.save_data()
                return True, f"✅ Deleted {deleted_count} attendance records for today!"
            else:
                return False, "❌ No attendance records found!"
        except Exception as e:
            return False, f"❌ Error: {str(e)}"
    
    def export_attendance_report(self, start_date=None, end_date=None):
        """Export attendance report for date range"""
        try:
            if start_date and end_date:
                filtered_data = self.attendance_df[
                    (self.attendance_df['Date'] >= str(start_date)) & 
                    (self.attendance_df['Date'] <= str(end_date))
                ]
                return filtered_data
            else:
                return self.attendance_df
        except Exception as e:
            st.error(f"Error generating report: {e}")
            return pd.DataFrame()

def generate_qr_code(student_id, name, year):
    """Generate a simple QR code image (simulated)"""
    # Create a simple image with student info
    img = Image.new('RGB', (200, 200), color='white')
    d = ImageDraw.Draw(img)
    
    # Draw a simple QR code pattern (in a real app, use a QR code library)
    for i in range(7):
        for j in range(7):
            if ((i == 0 or i == 6 or j == 0 or j == 6) or 
                (i > 1 and i < 5 and j > 1 and j < 5) or 
                (random.random() > 0.5)):
                d.rectangle([20 + i * 25, 20 + j * 25, 20 + i * 25 + 20, 20 + j * 25 + 20], fill='black')
    
    # Add student ID text
    d.text((100, 180), f"ID: {student_id}", fill='#1e3c72', anchor="mm")
    
    return img

def simulate_qr_scan():
    """Simulate QR code scanning"""
    users = [
        {'id': 'STU001', 'name': 'Rhea L. Reyes', 'role': 'Student', 'year': '3'},
        {'id': 'STU002', 'name': 'Angeluo John Padecio', 'role': 'Student', 'year': '3'},
        {'id': 'STU003', 'name': 'Althea Mae Aporador', 'role': 'Student', 'year': '3'},
        {'id': 'FAC001', 'name': 'Breig Cantila', 'role': 'Faculty', 'year': ''},
        {'id': 'FAC002', 'name': 'Joel Garcia', 'role': 'Faculty', 'year': ''},
    ]
    
    return random.choice(users)

def main():
    # Apply custom CSS
    apply_custom_css()
    
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.session_state.login_time = None
        st.session_state.signature_data = None
        st.session_state.fingerprint_verified = False
        st.session_state.attendance_records = []
        st.session_state.current_student_data = None
        st.session_state.scan_result = None
    
    # Initialize system
    if 'attendance_system' not in st.session_state:
        st.session_state.attendance_system = AttendanceSystem()
    
    system = st.session_state.attendance_system
    
    # Login page
    if not st.session_state.logged_in:
        show_login_page()
        return
    
    # Main application
    show_main_app(system)

def show_login_page():
    st.markdown("""
    <div style="display: flex; justify-content: center; align-items: center; height: 80vh;">
        <div style="background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.2); width: 90%; max-width: 500px;">
            <h2 style="text-align: center; color: #1e3c72; margin-bottom: 20px;">Login to Event Check Attendance System</h2>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submitted = st.form_submit_button("Login", use_container_width=True)
        
        if submitted:
            if username == "admin" and password == "password123":
                st.session_state.logged_in = True
                st.session_state.current_user = username
                st.session_state.login_time = datetime.now()
                st.rerun()
            else:
                st.error("Invalid credentials. Please try again.\n\nDemo credentials: admin / password123")
    
    st.markdown("""
            <div style="margin-top: 20px; text-align: center;">
                <p>Demo credentials: admin / password123</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_main_app(system):
    # Header
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("""
        <div class="main-header">
            <h1>Event Check Attendance System</h1>
            <p>You have successfully logged in to your account.</p>
            <p>Logged in at: {}</p>
        </div>
        """.format(st.session_state.login_time.strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="user-controls">
            <div style="display: flex; align-items: center;">
                <div class="user-avatar">{}</div>
                <button class="btn btn-logout" onclick="window.location.href='?logout=true'">Logout</button>
            </div>
        </div>
        """.format(st.session_state.current_user[0].upper()), unsafe_allow_html=True)
        
        # Handle logout
        if st.button("Logout", key="logout_btn"):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.login_time = None
            st.rerun()
    
    # Stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">142</div>
            <div class="stat-label">TOTAL USERS</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">67</div>
            <div class="stat-label">TODAY'S ATTENDANCE</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">89</div>
            <div class="stat-label">VERIFIED USERS</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Features
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h2 class="feature-title">QR Code Management</h2>
            <p class="feature-description">Generate and manage digital ID QR codes for students and staff.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Manage QR Codes", key="qr_btn", use_container_width=True):
            st.session_state.current_page = "qr_management"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h2 class="feature-title">Attendance Scanner</h2>
            <p class="feature-description">Scan QR codes to mark attendance and track student presence.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Open Scanner", key="scanner_btn", use_container_width=True):
            st.session_state.current_page = "scanner"
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h2 class="feature-title">Reports & Analytics</h2>
            <p class="feature-description">View attendance reports and analytics for better insights.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("View Reports", key="reports_btn", use_container_width=True):
            st.session_state.current_page = "reports"
            st.rerun()
    
    # Security Features
    st.markdown("""
    <div class="security-section">
        <h2 class="security-title">Security Features</h2>
        <div class="security-features" style="display: flex; justify-content: space-around; flex-wrap: wrap;">
            <div class="security-item">
                <div class="security-icon">✍️</div>
                <div class="security-label">Digital Signature</div>
                <div class="security-description">Secure digital signature verification for authentication</div>
            </div>
            <div class="security-item">
                <div class="security-icon">🔒</div>
                <div class="security-label">Fingerprint Authentication</div>
                <div class="security-description">Biometric fingerprint scanning for enhanced security</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Handle page navigation
    if 'current_page' in st.session_state:
        if st.session_state.current_page == "qr_management":
            show_qr_management(system)
        elif st.session_state.current_page == "scanner":
            show_scanner(system)
        elif st.session_state.current_page == "reports":
            show_reports(system)

def show_qr_management(system):
    st.header("QR Code Management")
    st.write("Generate and manage QR codes for students and staff.")
    
    # Student Information Form
    st.subheader("Student Information")
    col1, col2 = st.columns(2)
    
    with col1:
        student_id = st.text_input("Student ID", placeholder="Enter Student ID")
        student_name = st.text_input("Full Name", placeholder="Enter Full Name")
    
    with col2:
        student_year = st.selectbox("Year", ["", "Year 1", "Year 2", "Year 3", "Year 4"])
    
    if st.button("Generate QR Code", use_container_width=True):
        if student_id and student_name and student_year:
            st.session_state.current_student_data = {
                'id': student_id,
                'name': student_name,
                'year': student_year,
                'generated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Generate QR code
            qr_img = generate_qr_code(student_id, student_name, student_year)
            st.session_state.qr_image = qr_img
            
            st.success("QR Code generated successfully!")
        else:
            st.error("Please fill in all student information fields.")
    
    # Display student info if available
    if st.session_state.current_student_data:
        data = st.session_state.current_student_data
        
        st.markdown(f"""
        <div class="student-info">
            <h3 style="margin: 0 0 10px 0; color: #1e3c72;">Student Details</h3>
            <div class="student-details">
                <div class="student-detail">
                    <span class="student-label">Student ID:</span>
                    <span class="student-value">{data['id']}</span>
                </div>
                <div class="student-detail">
                    <span class="student-label">Name:</span>
                    <span class="student-value">{data['name']}</span>
                </div>
                <div class="student-detail">
                    <span class="student-label">Year:</span>
                    <span class="student-value">{data['year']}</span>
                </div>
                <div class="student-detail">
                    <span class="student-label">Generated:</span>
                    <span class="student-value">{data['generated']}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display QR code
        if 'qr_image' in st.session_state:
            st.image(st.session_state.qr_image, caption="Generated QR Code", use_column_width=False, width=200)
            
            # Download button
            buf = io.BytesIO()
            st.session_state.qr_image.save(buf, format="PNG")
            buf.seek(0)
            
            st.download_button(
                label="Download QR Code",
                data=buf,
                file_name=f"student-id-{data['id']}.png",
                mime="image/png",
                use_container_width=True
            )
    
    # Back button
    if st.button("Back to Dashboard", use_container_width=True):
        st.session_state.current_page = None
        st.rerun()

def show_scanner(system):
    st.header("Attendance Scanner")
    st.write("Position QR code within the frame to scan.")
    
    # Scanner container
    st.markdown("""
    <div class="scanner-container">
        <h3 style="text-align: center; color: #1e3c72;">QR Code Scanner</h3>
        <p style="text-align: center;">Scanner simulation - Click the button below to simulate scanning</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Start Scanner", use_container_width=True):
            # Simulate scanning
            scanned_user = simulate_qr_scan()
            scan_time = datetime.now().strftime("%H:%M:%S")
            
            # Add to attendance records
            attendance_record = {
                'id': scanned_user['id'],
                'name': scanned_user['name'],
                'role': scanned_user['role'],
                'year': scanned_user['year'],
                'time': scan_time,
                'status': 'Present'
            }
            
            if 'attendance_records' not in st.session_state:
                st.session_state.attendance_records = []
            
            st.session_state.attendance_records.insert(0, attendance_record)
            st.session_state.scan_result = attendance_record
            
            # Mark attendance in system
            system.mark_attendance(scanned_user['id'], scanned_user['name'], "QR Code")
    
    with col2:
        if st.button("Stop Scanner", use_container_width=True):
            st.session_state.scan_result = None
    
    # Display scan result
    if st.session_state.scan_result:
        result = st.session_state.scan_result
        
        st.markdown(f"""
        <div class="scan-result">
            <strong>QR Code Scanned Successfully!</strong>
            <div style="margin-top: 10px;">
                <div><strong>Name:</strong> {result['name']}</div>
                <div><strong>ID:</strong> {result['id']}</div>
                <div><strong>Role:</strong> {result['role']}</div>
                {f"<div><strong>Year:</strong> Year {result['year']}</div>" if result['year'] else ""}
                <div><strong>Time:</strong> {result['time']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Recent scans
    st.subheader("Recent Scans")
    if 'attendance_records' in st.session_state and st.session_state.attendance_records:
        for record in st.session_state.attendance_records[:5]:  # Show last 5 records
            year_text = f" - Year {record['year']}" if record['year'] else ""
            st.markdown(f"""
            <div class="attendance-item">
                <div>
                    <div class="attendance-name">{record['name']}</div>
                    <div class="attendance-time">{record['time']} - {record['role']}{year_text}</div>
                </div>
                <div class="status-badge status-present">{record['status']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No scans recorded yet.")
    
    # Back button
    if st.button("Back to Dashboard", key="scanner_back", use_container_width=True):
        st.session_state.current_page = None
        st.rerun()

def show_reports(system):
    st.header("Reports & Analytics")
    st.write("View detailed attendance reports and analytics.")
    
    # Statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Daily Attendance", "85%")
        st.markdown("""
        <div style="height: 20px; background: #e0e0e0; border-radius: 10px; overflow: hidden;">
            <div style="height: 100%; width: 85%; background: #1e3c72;"></div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.metric("Weekly Average", "78%")
        st.markdown("""
        <div style="height: 20px; background: #e0e0e0; border-radius: 10px; overflow: hidden;">
            <div style="height: 100%; width: 78%; background: #2a5298;"></div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.metric("Monthly Average", "82%")
        st.markdown("""
        <div style="height: 20px; background: #e0e0e0; border-radius: 10px; overflow: hidden;">
            <div style="height: 100%; width: 82%; background: #3a62a8;"></div>
        </div>
        """, unsafe_allow_html=True)
    
    # Export button
    if st.button("Export Report", use_container_width=True):
        st.success("Report exported successfully!")
    
    # Back button
    if st.button("Back to Dashboard", key="reports_back", use_container_width=True):
        st.session_state.current_page = None
        st.rerun()

if __name__ == "__main__":
    main()
