import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
import time as ti
import calendar as calInstitution
import os

st.title("CVR CANTEEN")
st.subheader("Welcome to CVR canteen page where you can order deleicious food by sitting at your place within minutes")

#domain=st.selectbox("Select your position: ",['Student','Manager','Faculty','Others'])
#st.write(f"You have selected {domain}.")

#Browse & Order: 
# View real-time digital menus, 
# see daily/weekly specials, and 
# place orders in advance or on the spot.'''

menu_data = {
    "Item": ["Samosa", "Burger", "Egg Puff","Egg Noodles","Veg Manchuria","Veg Noodles","Chicken Noodles","Weekly Special: Truffle Pasta", "Daily Special: Chicken Manchau Soup"],
    #"Category": ["Bakery", "Breakfast", "Beverages", "Weekly Special", "Daily Special"],
    "Price": [15,45,20,50,50,55,70,80,100],
    "Image": [
        "https://www.bing.com/images/search?view=detailv2&iss=sbi&FORM=recidp&sbisrc=ImgDropper&q=Samosa%20Recipe%20(Punjabi%20Potato%20Samosa)&imgurl=https://bing.com/th?id=OSK.39404795702b3e57be68dd57f9dfa608&idpbck=1&sim=4&pageurl=020fffb6cdae38315c4bfe2ade8338ef&filters=ForceHighConfRecipe:%22true%22&idpp=recipe", # Samosa
        "https://p325k7wa.twic.pics/high/burger-0f8c8574.jpg", # Burger
        "https://p325k7wa.twic.pics/high/puff-pastry-94e43f33.jpg", # Egg Puff
        "https://p325k7wa.twic.pics/high/noodles-6c5c0c9e.jpg", # Egg Noodles
        "https://p325k7wa.twic.pics/high/manchurian-4c28c688.jpg", # Manchuria
        "https://p325k7wa.twic.pics/high/veg-noodles-8a50b383.jpg", # Veg Noodles
        "https://p325k7wa.twic.pics/high/chicken-noodles-d1e9f1a2.jpg", # Chicken Noodles
        "https://p325k7wa.twic.pics/high/pasta-7e23f0a5.jpg", # Pasta
        "https://p325k7wa.twic.pics/high/soup-4a8f9d2c.jpg" # Soup
    ]
    #"Description": ["Freshly baked daily", "With chili flakes and lime", "Cold brew with creamy oat milk", "Limited time offer", "Seasonal favorite"]
}
df_menu = pd.DataFrame(menu_data)
#Login Page
st.set_page_config(page_title=" Login", page_icon="🔐")

def browse_order_page():
    # Sidebar for Logout and Cart
    with st.sidebar:
        st.title(f"👋 Hello, {st.session_state.user_role}!")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.cart = []
            st.rerun()
        
        st.divider()
        st.header("🛒 Your Order")
        if not st.session_state.cart:
            st.write("Cart is empty.")
        else:
            total = sum(item['price'] for item in st.session_state.cart)
            for item in st.session_state.cart:
                st.write(f"- {item['name']} (${item['price']:.2f})")
            st.subheader(f"Total: ${total:.2f}")
            if st.button("Confirm Order"):
                st.balloons()
                st.success("Order Sent to Kitchen!")
                st.session_state.cart = []
    
    # Display Menu
    st.header("🍽️ Menu")
    cols = st.columns(3)
    for idx, row in df_menu.iterrows():
        col = cols[idx % 3]
        with col:
            st.image(row['Image'], use_container_width=True)
            st.write(f"**{row['Item']}**")
            st.write(f"₹{row['Price']}")
            if st.button(f"Add to Cart", key=f"add_{idx}"):
                st.session_state.cart.append({"name": row['Item'], "price": row['Price']})
                st.success(f"{row['Item']} added to cart!")
                st.rerun()

def manager_page():
    # Manager Dashboard
    with st.sidebar:
        st.title(f"👋 Hello, {st.session_state.user_role}!")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_role = None
            st.rerun()
    
    st.write("### Manager Functions")
    st.write("- View all orders")
    st.write("- Manage menu items")
    st.write("- View sales reports")
    st.write("- Manage staff")

def faculty_page():
    # Faculty Dashboard
    with st.sidebar:
        st.title(f"👋 Hello, {st.session_state.user_role}!")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_role = None
            st.rerun()
    
    st.write("### Faculty Functions")
    st.write("- Browse menu and order food")
    st.write("- View order history")
    st.write("- Access nutritional information")
    
    # Display Menu
    st.header("🍽️ Menu")
    st.dataframe(df_menu, use_container_width=True)

def others_page():
    # Others Dashboard
    with st.sidebar:
        st.title(f"👋 Hello, {st.session_state.user_role}!")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_role = None
            st.rerun()
    
    st.write("### Guest Functions")
    st.write("- View menu")
    st.write("- Limited ordering options")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "cart" not in st.session_state:
    st.session_state.cart = []

if not st.session_state.logged_in:
    st.subheader("Please sign in to continue")

    with st.container(border=True):
        # Your requested domain selection
        domain = st.selectbox("Select your position: ", ['Student', 'Manager', 'Faculty', 'Others'])
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login", use_container_width=True):
            if username and (password == "123"):
                st.session_state.logged_in = True
                st.session_state.user_role = domain
                st.success(f"Logged in as {domain}!")
                st.rerun()
            else:
                st.error("Invalid Username or Password ")
else:
    st.header(f"{st.session_state.user_role} Dashboard")
    st.write(f"Welcome to the portal. You have selected **{st.session_state.user_role}** permissions.")
    
    if st.session_state.user_role == "Student":
        browse_order_page()
    elif st.session_state.user_role == "Manager":
        manager_page()
    elif st.session_state.user_role == "Faculty":
        faculty_page()
    else:
        others_page()