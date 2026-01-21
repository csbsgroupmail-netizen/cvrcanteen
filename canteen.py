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
        "sam.jfif",  # Samosa
        "burger.jfif",  # Burger
        "egg puff.jfif",  # Egg Puff
        "egg noodles.jfif",  # Egg Noodles
        "manchuria.jfif",  # Manchuria
        "veg noodles.jfif",  # Veg Noodles
        "chiken noodles.jfif",  # Chicken Noodles
        "pasta.jfif",  # Pasta
        "chicken manchou soup.jfif"  # Soup
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
                st.write(f"- {item['name']} (₹{item['price']:.2f})")
            st.subheader(f"Total: ₹{total:.2f}")
            if st.button("Confirm Order"):
                order = {
                    "order_id": len(st.session_state.orders) + 1,
                    "user_role": st.session_state.user_role,
                    "items": st.session_state.cart.copy(),
                    "total": total,
                    "timestamp": dt.datetime.now(),
                    "status": "Pending"
                }
                st.session_state.orders.append(order)
                st.balloons()
                
                order_details = f"""✅ Order Confirmed!

Order ID: #{order['order_id']}
Time: {order['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}

Items:
"""
                for item in order['items']:
                    order_details += f"  • {item['name']} - ₹{item['price']:.2f}\n"
                order_details += f"\nTotal: ₹{order['total']:.2f}"
                st.success(order_details)
                st.session_state.cart = []
                st.rerun()
    
    # Display Menu
    st.header("🍽️ Menu")
    cols = st.columns(3)
    for idx, row in df_menu.iterrows():
        col = cols[idx % 3]
        with col:
            if row['Image'] and os.path.exists(row['Image']):
                st.image(row['Image'], use_container_width=True)
            else:
                st.info(f"Image not found for {row['Item']}")
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
    
    st.write("### Manager Dashboard")
    st.write("Manage all orders, menu items, sales reports, and staff")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 View Orders", "📊 Sales Report", "🍽️ Manage Menu", "👥 Manage Staff"])
    
    with tab1:
        st.header("All Orders")
        if not st.session_state.orders:
            st.info("No orders yet")
        else:
            # Sort orders by timestamp (most recent first)
            sorted_orders = sorted(st.session_state.orders, key=lambda x: x['timestamp'], reverse=True)
            
            for order in sorted_orders:
                with st.container(border=True):
                    col1, col2, col3, col4 = st.columns([1, 2, 1, 1])
                    
                    with col1:
                        st.write(f"**Order #{order['order_id']}**")
                    
                    with col2:
                        st.write(f"Time: {order['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    with col3:
                        st.write(f"₹{order['total']:.2f}")
                    
                    with col4:
                        status_color = {
                            "Pending": "🟡",
                            "Preparing": "🔵",
                            "Ready": "🟢",
                            "Completed": "✅"
                        }
                        st.write(status_color.get(order['status'], "❓") + " " + order['status'])
                    
                    st.write(f"**Customer Type:** {order['user_role']}")
                    st.write("**Items:**")
                    for item in order['items']:
                        st.write(f"  • {item['name']} - ₹{item['price']:.2f}")
                    
                    col_status1, col_status2, col_status3, col_status4 = st.columns(4)
                    
                    with col_status1:
                        if st.button("Pending", key=f"pending_{order['order_id']}", use_container_width=True):
                            order['status'] = "Pending"
                            st.rerun()
                    
                    with col_status2:
                        if st.button("Preparing", key=f"preparing_{order['order_id']}", use_container_width=True):
                            order['status'] = "Preparing"
                            st.rerun()
                    
                    with col_status3:
                        if st.button("Ready", key=f"ready_{order['order_id']}", use_container_width=True):
                            order['status'] = "Ready"
                            st.rerun()
                    
                    with col_status4:
                        if st.button("Completed", key=f"completed_{order['order_id']}", use_container_width=True):
                            order['status'] = "Completed"
                            st.rerun()
    
    with tab2:
        st.header("Sales Report")
        if st.session_state.orders:
            total_sales = sum(order['total'] for order in st.session_state.orders)
            total_orders = len(st.session_state.orders)
            avg_order = total_sales / total_orders if total_orders > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Sales", f"₹{total_sales:.2f}")
            col2.metric("Total Orders", total_orders)
            col3.metric("Average Order Value", f"₹{avg_order:.2f}")
            
            st.subheader("Orders by Status")
            status_counts = {}
            for order in st.session_state.orders:
                status = order['status']
                status_counts[status] = status_counts.get(status, 0) + 1
            
            if status_counts:
                st.bar_chart(status_counts)
        else:
            st.info("No sales data yet")
    
    with tab3:
        st.header("Manage Menu")
        st.info("Menu management feature - You can add/edit/delete menu items here")
        st.write("Current Menu Items:", len(df_menu))
    
    with tab4:
        st.header("Manage Staff")
        st.info("Staff management feature - Manage staff members and their roles")

def faculty_page():
    # Faculty Dashboard
    with st.sidebar:
        st.title(f"👋 Hello, {st.session_state.user_role}!")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_role = None
            st.rerun()
        
        st.divider()
        st.header("🛒 Your Order")
        if not st.session_state.cart:
            st.write("Cart is empty.")
        else:
            total = sum(item['price'] for item in st.session_state.cart)
            for item in st.session_state.cart:
                st.write(f"- {item['name']} (₹{item['price']:.2f})")
            st.subheader(f"Total: ₹{total:.2f}")
            if st.button("Confirm Order"):
                order = {
                    "order_id": len(st.session_state.orders) + 1,
                    "user_role": st.session_state.user_role,
                    "items": st.session_state.cart.copy(),
                    "total": total,
                    "timestamp": dt.datetime.now(),
                    "status": "Pending"
                }
                st.session_state.orders.append(order)
                st.balloons()
                
                order_details = f"""✅ Order Confirmed!

Order ID: #{order['order_id']}
Time: {order['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}

Items:
"""
                for item in order['items']:
                    order_details += f"  • {item['name']} - ₹{item['price']:.2f}\n"
                order_details += f"\nTotal: ₹{order['total']:.2f}"
                st.success(order_details)
                st.session_state.cart = []
                st.rerun()
    
    st.write("### Faculty Functions")
    st.write("- Browse menu and order food")
    st.write("- View order history")
    st.write("- Access nutritional information")
    
    # Display Menu
    st.header("🍽️ Menu")
    cols = st.columns(3)
    for idx, row in df_menu.iterrows():
        col = cols[idx % 3]
        with col:
            if row['Image'] and os.path.exists(row['Image']):
                st.image(row['Image'], use_container_width=True)
            else:
                st.info(f"Image not found for {row['Item']}")
            st.write(f"**{row['Item']}**")
            st.write(f"₹{row['Price']}")
            if st.button(f"Add to Cart", key=f"faculty_add_{idx}"):
                st.session_state.cart.append({"name": row['Item'], "price": row['Price']})
                st.success(f"{row['Item']} added to cart!")
                st.rerun()

def others_page():
    # Others Dashboard
    with st.sidebar:
        st.title(f"👋 Hello, {st.session_state.user_role}!")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_role = None
            st.rerun()
        
        st.divider()
        st.header("🛒 Your Order")
        if not st.session_state.cart:
            st.write("Cart is empty.")
        else:
            total = sum(item['price'] for item in st.session_state.cart)
            for item in st.session_state.cart:
                st.write(f"- {item['name']} (₹{item['price']:.2f})")
            st.subheader(f"Total: ₹{total:.2f}")
            if st.button("Confirm Order"):
                order = {
                    "order_id": len(st.session_state.orders) + 1,
                    "user_role": st.session_state.user_role,
                    "items": st.session_state.cart.copy(),
                    "total": total,
                    "timestamp": dt.datetime.now(),
                    "status": "Pending"
                }
                st.session_state.orders.append(order)
                st.balloons()
                
                order_details = f"""✅ Order Confirmed!

Order ID: #{order['order_id']}
Time: {order['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}

Items:
"""
                for item in order['items']:
                    order_details += f"  • {item['name']} - ₹{item['price']:.2f}\n"
                order_details += f"\nTotal: ₹{order['total']:.2f}"
                st.success(order_details)
                st.session_state.cart = []
                st.rerun()
    
    st.write("### Guest Functions")
    st.write("- View menu")
    st.write("- Limited ordering options")
    
    # Display Menu
    st.header("🍽️ Menu")
    cols = st.columns(3)
    for idx, row in df_menu.iterrows():
        col = cols[idx % 3]
        with col:
            if row['Image'] and os.path.exists(row['Image']):
                st.image(row['Image'], use_container_width=True)
            else:
                st.info(f"Image not found for {row['Item']}")
            st.write(f"**{row['Item']}**")
            st.write(f"₹{row['Price']}")
            if st.button(f"Add to Cart", key=f"others_add_{idx}"):
                st.session_state.cart.append({"name": row['Item'], "price": row['Price']})
                st.success(f"{row['Item']} added to cart!")
                st.rerun()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "cart" not in st.session_state:
    st.session_state.cart = []
if "orders" not in st.session_state:
    st.session_state.orders = []

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
