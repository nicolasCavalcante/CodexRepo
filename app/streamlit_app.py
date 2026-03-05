import os

import pandas as pd
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000/v1")

st.set_page_config(page_title="CRUD + Analytics", layout="wide")
st.title("CRUD + Analytics Platform")

tab_users, tab_products, tab_orders = st.tabs(["Users", "Products", "Orders"])

with tab_users:
    st.subheader("Create user")
    with st.form("create-user"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        submitted = st.form_submit_button("Create")
        if submitted:
            res = requests.post(f"{API_URL}/users", json={"name": name, "email": email}, timeout=10)
            st.success(f"Created: {res.json().get('id')}") if res.ok else st.error(res.text)

    users = requests.get(f"{API_URL}/users", timeout=10)
    if users.ok:
        st.dataframe(pd.DataFrame(users.json()), use_container_width=True)

with tab_products:
    st.subheader("Create product")
    with st.form("create-product"):
        sku = st.text_input("SKU")
        product_name = st.text_input("Product name")
        price = st.number_input("Price", min_value=0.01)
        submitted = st.form_submit_button("Create")
        if submitted:
            res = requests.post(
                f"{API_URL}/products", json={"sku": sku, "name": product_name, "price": price}, timeout=10
            )
            st.success(f"Created: {res.json().get('id')}") if res.ok else st.error(res.text)

    products = requests.get(f"{API_URL}/products", timeout=10)
    if products.ok:
        st.dataframe(pd.DataFrame(products.json()), use_container_width=True)

with tab_orders:
    st.subheader("Create order")
    with st.form("create-order"):
        user_id = st.number_input("User ID", min_value=1, step=1)
        product_id = st.number_input("Product ID", min_value=1, step=1)
        qty = st.number_input("Quantity", min_value=1, step=1)
        submitted = st.form_submit_button("Create")
        if submitted:
            res = requests.post(
                f"{API_URL}/orders", json={"user_id": user_id, "product_id": product_id, "quantity": qty}, timeout=10
            )
            st.success(f"Created: {res.json().get('id')}") if res.ok else st.error(res.text)

    orders = requests.get(f"{API_URL}/orders", timeout=10)
    if orders.ok:
        st.dataframe(pd.DataFrame(orders.json()), use_container_width=True)
