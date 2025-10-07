import streamlit as st
import json
import os
from datetime import datetime
import plotly.graph_objects as go

DATA_FILE = "users_data.json"

def load_users_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def initialize_session_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "current_pin" not in st.session_state:
        st.session_state.current_pin = None
    if "budget" not in st.session_state:
        st.session_state.budget = 0.0
    if "expenses" not in st.session_state:
        st.session_state.expenses = []
    if "backup" not in st.session_state:
        st.session_state.backup = None

def login_page():
    st.title("Secure Login")
    pin = st.text_input("Enter PIN", type="password")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            users = load_users_data()
            if pin in users:
                st.session_state.logged_in = True
                st.session_state.current_pin = pin
                st.session_state.budget = users[pin].get("budget", 0.0)
                st.session_state.expenses = users[pin].get("expenses", [])
                st.success("Logged in successfully!")
                st.experimental_rerun()
            else:
                st.error("PIN not found!")
    with col2:
        if st.button("Register"):
            if not pin:
                st.warning("Enter a PIN to register!")
            else:
                users = load_users_data()
                if pin in users:
                    st.error("PIN already exists!")
                else:
                    users[pin] = {"budget": 0.0, "expenses": []}
                    save_users_data(users)
                    st.session_state.logged_in = True
                    st.session_state.current_pin = pin
                    st.session_state.budget = 0.0
                    st.session_state.expenses = []
                    st.success("PIN registered — you are now logged in.")
                    st.experimental_rerun()

def save_data():
    if not st.session_state.current_pin:
        return
    users = load_users_data()
    users[st.session_state.current_pin] = {
        "budget": st.session_state.budget,
        "expenses": st.session_state.expenses
    }
    save_users_data(users)

def dashboard():
    st.header("Weekly Grocery Budget & Expense Manager")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_pin = None
        st.session_state.budget = 0.0
        st.session_state.expenses = []
        st.session_state.backup = None
        st.experimental_rerun()

    # Budget setting form
    with st.form("budget_form", clear_on_submit=False):
        budget_input = st.number_input("Set Weekly Budget (₱)", min_value=0.0, value=st.session_state.budget, step=0.01, format="%.2f")
        submitted_budget = st.form_submit_button("Set Budget")
        if submitted_budget:
            if budget_input <= 0:
                st.warning("Enter a valid budget!")
            else:
                st.session_state.budget = budget_input
                save_data()
                st.success("Budget set successfully!")

    # Expense adding form
    with st.form("expense_form", clear_on_submit=True):
        item = st.text_input("Item name")
        category = st.selectbox("Category", ["School Expenses", "Grocery", "Hang-outs", "Emergencies", "Others"])
        amount = st.number_input("Amount (₱)", min_value=0.0, step=0.01, format="%.2f")
        current_year = datetime.now().year
        year = st.selectbox("Year", list(range(current_year - 5, current_year + 6)), index=5)
        month = st.selectbox("Month", ["January", "February", "March", "April", "May", "June",
                                      "July", "August", "September", "October", "November", "December"])
        week = st.selectbox("Week", ["Week 1 (1–7)", "Week 2 (8–14)", "Week 3 (15–21)", "Week 4 (22–28)", "Week 5 (29–31)"])
        submitted_expense = st.form_submit_button("Add Expense")
        if submitted_expense:
            if not item.strip():
                st.warning("Enter an item name!")
            elif amount <= 0:
                st.warning("Enter a valid amount!")
            else:
                expense = {
                    "item": item.strip(),
                    "category": category,
                    "amount": amount,
                    "year": year,
                    "month": month,
                    "week": week
                }
                st.session_state.expenses.append(expense)
                save_data()
                st.success("Expense added successfully!")

    # Display summary cards
    spent = sum(e["amount"] for e in st.session_state.expenses)
    remaining = st.session_state.budget - spent

    col1, col2, col3 = st.columns(3)
    col1.metric("Weekly Budget (₱)", f"{st.session_state.budget:.2f}")
    col2.metric("Spent (₱)", f"{spent:.2f}")
    if remaining < 0:
        col3.metric("Remaining (₱)", f"{remaining:.2f}", delta_color="inverse")
    else:
        col3.metric("Remaining (₱)", f"{remaining:.2f}")

    # Display expenses table
    if st.session_state.expenses:
        st.subheader("Expenses")
        st.table(st.session_state.expenses)
    else:
        st.info("No expenses yet")

    # Pie chart for spending by category
    if st.session_state.expenses:
        st.subheader("Spending Overview")
        categories = list(set(e["category"] for e in st.session_state.expenses))
        spent_by_category = []
        for cat in categories:
            total = sum(e["amount"] for e in st.session_state.expenses if e["category"] == cat)
            spent_by_category.append(total)

        fig = go.Figure(data=[go.Pie(labels=categories, values=spent_by_category, hole=0.3,
                                     textinfo='percent+label', insidetextorientation='radial')])
        st.plotly_chart(fig, use_container_width=True)

    # Weekly advice card
    if st.session_state.budget > 0:
        st.subheader("Weekly Advice")
        if spent > st.session_state.budget:
            st.error("⚠️ Over budget — cut down on groceries.")
        else:
            st.success("✅ Within budget — keep it up!")

    # Reset and restore buttons
    col_reset, col_restore = st.columns(2)
    with col_reset:
        if st.button("Reset All"):
            st.session_state.backup = {
                "budget": st.session_state.budget,
                "expenses": st.session_state.expenses.copy()
            }
            st.session_state.budget = 0.0
            st.session_state.expenses = []
            save_data()
            st.success("All data reset. Use 'Restore' to undo.")
    with col_restore:
        if st.button("Restore"):
            if st.session_state.backup:
                st.session_state.budget = st.session_state.backup["budget"]
                st.session_state.expenses = st.session_state.backup["expenses"]
                save_data()
                st.success("Data restored successfully!")
            else:
                st.warning("No backup found!")

def main():
    st.set_page_config(page_title="Weekly Grocery Budget & Expense Manager")
    initialize_session_state()
    if not st.session_state.logged_in:
        login_page()
    else:
        dashboard()

if _name_ == "_main_":
    main()
