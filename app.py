# app.py
import streamlit as st
from bank import Bank

Bank.load_data()

st.title("Bank Management System")

menu = st.sidebar.selectbox("Choose Action", [
    "Create Account", "Deposit Money", "Withdraw Money",
    "Show Details", "Update Details", "Delete Account"
])

if menu == "Create Account":
    st.header("Create New Account")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0)
    email = st.text_input("Email")
    pin = st.text_input("4-digit PIN", type="password")
    if st.button("Create"):
        if pin.isdigit():
            result, msg = Bank.create_account(name, age, email, int(pin))
            st.success(msg)
            if result:
                st.json(result)
        else:
            st.error("PIN must be numeric")

elif menu == "Deposit Money":
    st.header("Deposit Money")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amt = st.number_input("Amount", min_value=1)
    if st.button("Deposit"):
        success, msg = Bank.deposit(acc, int(pin), amt)
        st.success(msg) if success else st.error(msg)

elif menu == "Withdraw Money":
    st.header("Withdraw Money")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amt = st.number_input("Amount", min_value=1)
    if st.button("Withdraw"):
        success, msg = Bank.withdraw(acc, int(pin), amt)
        st.success(msg) if success else st.error(msg)

elif menu == "Show Details":
    st.header("Account Details")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    if st.button("Show"):
        user = Bank.get_details(acc, int(pin))
        if user:
            st.json(user)
        else:
            st.error("Account not found")

elif menu == "Update Details":
    st.header("Update Account Details")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    name = st.text_input("New Name")
    email = st.text_input("New Email")
    new_pin = st.text_input("New PIN")
    if st.button("Update"):
        success, msg = Bank.update_details(acc, int(pin), name, email, new_pin)
        st.success(msg) if success else st.error(msg)

elif menu == "Delete Account":
    st.header("Delete Account")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    if st.button("Delete"):
        success, msg = Bank.delete_account(acc, int(pin))
        st.success(msg) if success else st.error(msg)
