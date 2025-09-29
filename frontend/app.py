import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Define the base URL for the backend API
BACKEND_URL = "http://backend:8000"

# --- Page Configuration ---
st.set_page_config(
    page_title="Reliant Windows ERP/CRM",
    page_icon="🏠",
    layout="wide"
)

# --- Initialize session state for editing ---
if 'customer_to_edit' not in st.session_state:
    st.session_state.customer_to_edit = None

# --- Main Application UI ---
st.title("Reliant Windows ERP/CRM Prototype")

# --- Tabbed Interface ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 AI Price Predictor", "👥 Customer Management", "📋 Quotation History", "👤 User Management"])

# --- Tab 1: AI Price Predictor ---
with tab1:
    st.header("AI-Powered Quotation Predictor")
    st.write("Get an instant price estimate for a single item using our trained AI model.")

    with st.form("prediction_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            product_type = st.selectbox("Product Type", options=["Window", "Door"])
            width = st.number_input("Width (meters)", min_value=0.5, max_value=5.0, value=1.2, step=0.1)
        with col2:
            material = st.selectbox("Material", options=["uPVC", "Aluminium", "Timber"])
            height = st.number_input("Height (meters)", min_value=0.5, max_value=3.0, value=1.5, step=0.1)
        with col3:
            st.write("") 
            st.write("")
            quantity = st.number_input("Quantity", min_value=1, max_value=20, value=1, step=1)
            
        predict_button = st.form_submit_button("Predict Price")

    if predict_button:
        payload = {
            "width": width, "height": height, "quantity": quantity,
            "product_type": product_type, "material": material
        }
        try:
            with st.spinner("Getting AI prediction..."):
                response = requests.post(f"{BACKEND_URL}/predict_quote", json=payload)
                response.raise_for_status()
                prediction = response.json()
                price = prediction.get("predicted_price", 0)
                st.success(f"**Predicted Price:** £{price:,.2f}")
        except requests.exceptions.RequestException as e:
            st.error("Failed to communicate with the backend API.")
            st.warning("Could not connect to the backend. Please ensure all services are running correctly.")

# --- Tab 2: Customer Management ---
with tab2:
    st.header("Customer Relationship Management")
    
    with st.form("new_customer_form", clear_on_submit=True):
        st.subheader("Add a New Customer")
        col1, col2 = st.columns(2)
        with col1:
            new_name = st.text_input("Full Name*")
            new_email = st.text_input("Email Address*")
        with col2:
            new_phone = st.text_input("Phone Number*")
            new_address = st.text_area("Address (Optional)")
        
        add_customer_button = st.form_submit_button("Add Customer")

    if add_customer_button:
        if new_name and new_email and new_phone:
            payload = {
                "full_name": new_name, "email": new_email,
                "phone_number": new_phone, "address": new_address
            }
            try:
                response = requests.post(f"{BACKEND_URL}/customers/", json=payload)
                response.raise_for_status()
                st.success(f"Customer '{new_name}' added successfully!")
                st.balloons()
            except requests.exceptions.RequestException as e:
                st.error(f"Error adding customer: {e.response.json().get('detail', 'Unknown error')}")
        else:
            st.warning("Please fill in all required fields (*).")

    st.divider()
    
    # --- CORRECTED: This section has been restored ---
    st.subheader("Find a Customer")
    search_method = st.radio("Search by:", ("ID", "Full Name"), horizontal=True, key="search_method")

    if search_method == "ID":
        search_id = st.number_input("Enter Customer ID", min_value=1, step=1, key="search_id_input")
        if st.button("Search by ID"):
            try:
                with st.spinner(f"Searching for customer with ID {search_id}..."):
                    response = requests.get(f"{BACKEND_URL}/customers/{search_id}")
                    if response.status_code == 200:
                        customer = response.json()
                        st.success("Customer found!")
                        st.json(customer)
                    else:
                        st.warning(f"No customer found with ID {search_id}.")
            except requests.exceptions.RequestException:
                st.error("Failed to communicate with the backend.")

    elif search_method == "Full Name":
        search_name = st.text_input("Enter Full Name (or part of it)", key="search_name_input")
        if st.button("Search by Name"):
            if search_name:
                try:
                    with st.spinner(f"Searching for customers named '{search_name}'..."):
                        response = requests.get(f"{BACKEND_URL}/customers/")
                        response.raise_for_status()
                        customers = response.json()
                        results = [c for c in customers if search_name.lower() in c['full_name'].lower()]
                        
                        if results:
                            st.success(f"Found {len(results)} matching customer(s).")
                            st.dataframe(pd.DataFrame(results), use_container_width=True)
                        else:
                            st.warning(f"No customers found matching '{search_name}'.")
                except requests.exceptions.RequestException:
                    st.error("Failed to communicate with the backend.")
            else:
                st.warning("Please enter a name to search.")

    st.divider()

    st.subheader("Update Customer Details")
    update_id = st.number_input("Enter Customer ID to Edit", min_value=1, step=1, key="update_id_input")

    if st.button("Find Customer to Edit"):
        if update_id:
            try:
                with st.spinner(f"Finding customer {update_id}..."):
                    response = requests.get(f"{BACKEND_URL}/customers/{update_id}")
                    if response.status_code == 200:
                        st.session_state.customer_to_edit = response.json()
                    else:
                        st.session_state.customer_to_edit = None
                        st.warning(f"No customer found with ID {update_id}.")
            except requests.exceptions.RequestException:
                st.session_state.customer_to_edit = None
                st.error("Failed to communicate with backend.")

    if st.session_state.customer_to_edit:
        customer = st.session_state.customer_to_edit
        with st.form("update_customer_form"):
            st.write(f"**Editing:** {customer['full_name']} (ID: {customer['id']})")
            updated_name = st.text_input("Full Name", value=customer.get('full_name', ''))
            updated_email = st.text_input("Email Address", value=customer.get('email', ''))
            updated_phone = st.text_input("Phone Number", value=customer.get('phone_number', ''))
            updated_address = st.text_area("Address", value=customer.get('address', ''))
            
            update_button = st.form_submit_button("Save Changes")
            if update_button:
                payload = {
                    "full_name": updated_name, "email": updated_email,
                    "phone_number": updated_phone, "address": updated_address
                }
                try:
                    with st.spinner("Updating customer..."):
                        response = requests.put(f"{BACKEND_URL}/customers/{customer['id']}", json=payload)
                        response.raise_for_status()
                        st.success("Customer details updated successfully!")
                        st.balloons()
                        st.session_state.customer_to_edit = None
                except requests.exceptions.RequestException as e:
                    st.error(f"Error updating customer: {e.response.json().get('detail', 'Unknown error')}")

    st.divider()
    st.subheader("Current Customer List")
    try:
        response = requests.get(f"{BACKEND_URL}/customers/")
        response.raise_for_status()
        customers = response.json()
        if customers:
            df = pd.DataFrame(customers)
            st.dataframe(df[['id', 'full_name', 'email', 'phone_number', 'address']], use_container_width=True)
        else:
            st.info("No customers found in the database yet.")
    except requests.exceptions.RequestException:
        st.error("Could not fetch customer list from the backend.")

# --- Tab 3: View Quotation History ---
with tab3:
    st.header("View Customer Quotation History")
    
    customer_id_input = st.number_input("Enter Customer ID", min_value=1, step=1, key="history_customer_id")
    
    if st.button("Fetch Quotation History"):
        if customer_id_input:
            with st.spinner(f"Fetching history for customer ID {customer_id_input}..."):
                try:
                    quote_response = requests.get(f"{BACKEND_URL}/customers/{customer_id_input}/quotations/")
                    
                    if quote_response.status_code == 404:
                         st.warning(f"No customer found with ID {customer_id_input}.")
                    else:
                        quote_response.raise_for_status()
                        quotes = quote_response.json()
                        
                        if not quotes:
                            st.warning("No quotations found for this customer.")
                        else:
                            st.success(f"Found {len(quotes)} quotations for Customer ID {customer_id_input}.")
                            for quote in quotes:
                                total_price = float(quote.get('total_price', 0) or 0)
                                created_date = pd.to_datetime(quote['created_at']).strftime('%d %B %Y')
                                
                                with st.expander(f"Quotation ID: {quote['id']} - Status: {quote['status']} - Total: £{total_price:,.2f}"):
                                    st.write(f"Created on: {created_date}")
                                    st.write("**Items in this Quotation:**")
                                    if quote['items']:
                                        items_df = pd.DataFrame(quote['items'])
                                        st.dataframe(items_df[['product_id', 'width', 'height', 'quantity', 'price']], use_container_width=True)
                                    else:
                                        st.write("No items found for this quotation.")
                except requests.exceptions.RequestException:
                    st.error("Failed to communicate with the backend. Please ensure all services are running correctly.")

# --- Tab 4: User Management ---
with tab4:
    st.header("👤 User Management")
    st.write("This section is for authorized administrators to manage user roles.")

    with st.form("role_update_form", clear_on_submit=True):
        st.subheader("Change a User's Role")
        
        st.info("You must provide your administrator credentials to perform this action.", icon="🔐")
        
        col1, col2 = st.columns(2)
        with col1:
            admin_username = st.text_input("Your Admin Username")
            admin_password = st.text_input("Your Admin Password", type="password")
        with col2:
            target_user_id = st.number_input("Target User ID to Modify", min_value=1, step=1)
            new_role = st.selectbox("New Role to Assign", 
                                    options=[
                                        "Manager", "Regional Manager", "Sales", 
                                        "Construction Worker", "Human Resources Head", 
                                        "Human Resources Associate"
                                    ])

        submit_role_change = st.form_submit_button("Update Role")

    if submit_role_change:
        if not all([admin_username, admin_password, target_user_id, new_role]):
            st.warning("Please fill in all fields.")
        else:
            payload = {
                "admin_username": admin_username,
                "admin_password": admin_password,
                "target_user_id": target_user_id,
                "new_role": new_role
            }
            try:
                with st.spinner(f"Attempting to change role for user {target_user_id}..."):
                    response = requests.put(f"{BACKEND_URL}/users/update-role", json=payload)
                    response.raise_for_status()
                    st.success(f"Successfully updated role for user ID {target_user_id}!")
                    st.balloons()
            except requests.exceptions.RequestException as e:
                if e.response.status_code == 401:
                    st.error("Authentication failed. Please check your admin username and password.")
                elif e.response.status_code == 403:
                    st.error("Authorization failed. You do not have the required 'Human Resources Head' privileges.")
                elif e.response.status_code == 404:
                    st.error(f"Action failed. The target user with ID {target_user_id} was not found.")
                else:
                    st.error(f"An unexpected error occurred: {e.response.json().get('detail', 'Unknown error')}")

    st.divider()
    st.subheader("Current User List")
    
    st.write("Enter your admin credentials to view the full list of users.")
    with st.form("view_users_form"):
        view_admin_user = st.text_input("Your Admin Username", key="view_user_admin_name")
        view_admin_pass = st.text_input("Your Admin Password", type="password", key="view_user_admin_pass")
        view_users_button = st.form_submit_button("View All Users")
        
    if view_users_button:
        if view_admin_user and view_admin_pass:
            try:
                with st.spinner("Fetching user list..."):
                    params = {"admin_username": view_admin_user, "admin_password": view_admin_pass}
                    response = requests.get(f"{BACKEND_URL}/users/", params=params)
                    response.raise_for_status()
                    users = response.json()
                    st.dataframe(pd.DataFrame(users), use_container_width=True)
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to fetch users: {e.response.json().get('detail', 'Access denied or invalid credentials.')}")
        else:
            st.warning("Please provide admin credentials to view the user list.")

