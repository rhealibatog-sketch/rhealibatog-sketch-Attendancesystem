import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
import os
import json

# Page configuration
st.set_page_config(
    page_title="Even Check Attendance System",
    page_icon="📋",
    layout="wide"
)

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

def main():
    st.title("📋 Even Check Attendance System")
    st.markdown("---")
    
    # Initialize system
    if 'attendance_system' not in st.session_state:
        st.session_state.attendance_system = AttendanceSystem()
    
    system = st.session_state.attendance_system
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", [
        "🏠 Dashboard", 
        "📝 Mark Attendance", 
        "👥 Manage Students",
        "📊 Reports & Analytics"
    ])
    
    if page == "🏠 Dashboard":
        show_dashboard(system)
    elif page == "📝 Mark Attendance":
        show_mark_attendance(system)
    elif page == "👥 Manage Students":
        show_manage_students(system)
    elif page == "📊 Reports & Analytics":
        show_reports(system)

def show_dashboard(system):
    st.header("🏠 Dashboard Overview")
    
    # Quick stats in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_records = len(system.attendance_df)
        st.metric("Total Records", total_records)
    
    with col2:
        unique_students = system.attendance_df['StudentID'].nunique() if not system.attendance_df.empty else 0
        st.metric("Unique Students", unique_students)
    
    with col3:
        total_days = system.attendance_df['Date'].nunique() if not system.attendance_df.empty else 0
        st.metric("Total Days", total_days)
    
    with col4:
        registered_students = len(system.students_data)
        st.metric("Registered Students", registered_students)
    
    st.markdown("---")
    
    # Today's attendance
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📅 Today's Attendance")
        today_data = system.get_today_attendance()
        
        if not today_data.empty:
            st.dataframe(today_data[['StudentID', 'Name', 'Time', 'Method']], 
                        use_container_width=True,
                        height=300)
        else:
            st.info("No attendance marked today")
    
    with col2:
        st.subheader("🚀 Quick Actions")
        
        if st.button("📝 Mark Attendance", use_container_width=True, type="primary"):
            st.rerun()
        
        if st.button("👥 Add Student", use_container_width=True):
            st.rerun()
        
        if st.button("📊 View Reports", use_container_width=True):
            st.rerun()
        
        # Recent activity
        st.subheader("📈 Recent Activity")
        if not system.attendance_df.empty:
            recent = system.attendance_df.tail(3)
            for _, row in recent.iterrows():
                st.write(f"**{row['Name']}** - {row['Time']}")

def show_mark_attendance(system):
    st.header("📝 Mark Attendance")
    
    # Use form for better user experience
    with st.form("attendance_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            student_id = st.text_input("Student ID *", 
                                     placeholder="Enter Student ID",
                                     help="Required field")
            name = st.text_input("Student Name *", 
                               placeholder="Enter full name",
                               help="Required field")
        
        with col2:
            method = st.selectbox("Method", 
                                ["Manual", "QR Code", "Biometric", "Facial Recognition"])
            department = st.selectbox("Department", 
                                    ["Computer Science", "Electrical", "Mechanical", "Civil", "Other", "Not Specified"])
        
        submitted = st.form_submit_button("✅ Mark Attendance", use_container_width=True)
        
        if submitted:
            if student_id.strip() and name.strip():
                success, message = system.mark_attendance(student_id, name, method)
                if success:
                    st.success(message)
                    st.balloons()
                    
                    # Automatically add to students if not exists
                    if student_id not in system.students_data:
                        system.add_student(student_id, name, department)
                        st.info(f"Student {name} automatically added to registry")
                else:
                    st.warning(message)
            else:
                st.error("❌ Please enter both Student ID and Name")
    
    st.markdown("---")
    
    # Today's summary
    st.subheader("📊 Today's Summary")
    today_data = system.get_today_attendance()
    
    if not today_data.empty:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Today", len(today_data))
        
        with col2:
            st.metric("Unique Students", today_data['StudentID'].nunique())
        
        with col3:
            methods_count = today_data['Method'].value_counts()
            most_common = methods_count.index[0] if not methods_count.empty else "N/A"
            st.metric("Most Common Method", most_common)
        
        # Show today's records
        with st.expander("View Today's Detailed Records"):
            st.dataframe(today_data, use_container_width=True)
    else:
        st.info("No attendance marked today yet")

def show_manage_students(system):
    st.header("👥 Manage Students")
    
    tab1, tab2, tab3 = st.tabs(["➕ Add Student", "📋 View Students", "🔍 Student Details"])
    
    with tab1:
        st.subheader("Add New Student")
        
        with st.form("add_student_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                student_id = st.text_input("Student ID *", 
                                         help="Unique identifier for the student")
                full_name = st.text_input("Full Name *", 
                                        help="Student's complete name")
            
            with col2:
                department = st.selectbox("Department", 
                                        ["Computer Science", "Electrical", "Mechanical", "Civil", "Business", "Arts", "Other"])
                year = st.selectbox("Year", ["1st", "2nd", "3rd", "4th", "Graduate"])
            
            submitted = st.form_submit_button("➕ Add Student", use_container_width=True)
            
            if submitted:
                if student_id.strip() and full_name.strip():
                    success, message = system.add_student(student_id, full_name, department)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
                else:
                    st.error("❌ Please fill in all required fields (*)")
    
    with tab2:
        st.subheader("Registered Students")
        
        if system.students_data:
            # Convert to DataFrame for better display
            students_list = []
            for student_id, info in system.students_data.items():
                students_list.append({
                    'Student ID': student_id,
                    'Name': info['name'],
                    'Department': info.get('department', 'Not Specified'),
                    'Added Date': info.get('added_date', 'Unknown')
                })
            
            students_df = pd.DataFrame(students_list)
            
            # Search and filter
            search_term = st.text_input("🔍 Search students by name or ID:")
            if search_term:
                filtered_students = students_df[
                    students_df['Name'].str.contains(search_term, case=False, na=False) |
                    students_df['Student ID'].astype(str).str.contains(search_term, case=False, na=False)
                ]
                st.dataframe(filtered_students, use_container_width=True)
            else:
                st.dataframe(students_df, use_container_width=True)
            
            # Statistics
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Students", len(students_df))
            with col2:
                dept_counts = students_df['Department'].value_counts()
                most_common_dept = dept_counts.index[0] if not dept_counts.empty else "N/A"
                st.metric("Most Common Department", most_common_dept)
            
            # Export functionality
            st.subheader("Export Data")
            csv_data = students_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Students List as CSV",
                data=csv_data,
                file_name="students_list.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.info("No students registered yet. Add some students to get started!")
    
    with tab3:
        st.subheader("Student Attendance Details")
        
        student_lookup = st.text_input("Enter Student ID to view attendance history:")
        
        if student_lookup:
            student_attendance = system.get_student_attendance(student_lookup)
            student_info = system.students_data.get(student_lookup, {})
            
            if student_info:
                st.write(f"**Student:** {student_info.get('name', 'N/A')}")
                st.write(f"**Department:** {student_info.get('department', 'N/A')}")
                
                if not student_attendance.empty:
                    st.dataframe(student_attendance, use_container_width=True)
                    
                    # Attendance statistics
                    total_days = len(student_attendance)
                    present_days = len(student_attendance[student_attendance['Status'] == 'Present'])
                    attendance_rate = (present_days / total_days * 100) if total_days > 0 else 0
                    
                    st.metric("Attendance Rate", f"{attendance_rate:.1f}%")
                else:
                    st.info("No attendance records found for this student")
            else:
                st.warning("Student not found in registry")

def show_reports(system):
    st.header("📊 Reports & Analytics")
    
    if system.attendance_df.empty:
        st.info("No data available for reports. Mark some attendance first!")
        return
    
    # Overall statistics
    st.subheader("📈 Overall Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_records = len(system.attendance_df)
        st.metric("Total Records", total_records)
    
    with col2:
        unique_students = system.attendance_df['StudentID'].nunique()
        st.metric("Unique Students", unique_students)
    
    with col3:
        total_days = system.attendance_df['Date'].nunique()
        st.metric("Total Days", total_days)
    
    with col4:
        avg_daily = total_records / total_days if total_days > 0 else 0
        st.metric("Avg Daily Attendance", f"{avg_daily:.1f}")
    
    st.markdown("---")
    
    # Visualization section
    st.subheader("📊 Visual Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Method Distribution**")
        method_counts = system.attendance_df['Method'].value_counts()
        if not method_counts.empty:
            st.bar_chart(method_counts)
        else:
            st.info("No method data available")
    
    with col2:
        st.write("**Daily Attendance Trend**")
        daily_counts = system.attendance_df.groupby('Date').size()
        if not daily_counts.empty:
            st.line_chart(daily_counts)
        else:
            st.info("No daily data available")
    
    # Advanced filtering
    st.markdown("---")
    st.subheader("🔍 Advanced Reports")
    
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input("Start Date", 
                                 value=date.today() - timedelta(days=30))
    
    with col2:
        end_date = st.date_input("End Date", value=date.today())
    
    if st.button("Generate Custom Report", use_container_width=True):
        filtered_data = system.attendance_df[
            (system.attendance_df['Date'] >= str(start_date)) & 
            (system.attendance_df['Date'] <= str(end_date))
        ]
        
        if not filtered_data.empty:
            st.write(f"**Report for {start_date} to {end_date}:**")
            st.dataframe(filtered_data, use_container_width=True)
            
            # Export custom report
            csv_data = filtered_data.to_csv(index=False)
            st.download_button(
                label="📥 Download Custom Report",
                data=csv_data,
                file_name=f"attendance_report_{start_date}_to_{end_date}.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.info("No records found for the selected date range")
    
    # Quick exports
    st.markdown("---")
    st.subheader("📥 Data Export")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Export full attendance data
        full_csv = system.attendance_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Full Attendance Data",
            data=full_csv,
            file_name="full_attendance_data.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        # Export today's data
        today_data = system.get_today_attendance()
        if not today_data.empty:
            today_csv = today_data.to_csv(index=False)
            st.download_button(
                label="📥 Download Today's Data",
                data=today_csv,
                file_name=f"attendance_{date.today()}.csv",
                mime="text/csv",
                use_container_width=True
            )

if __name__ == "__main__":
    main()