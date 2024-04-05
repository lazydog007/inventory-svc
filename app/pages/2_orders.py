# Display inventory related content
import pandas as pd
import requests
import streamlit as st
# Define the base URL of your API
base_url = 'http://localhost:8000'  # Update with your API URL

# Define Streamlit app layout
st.title('Ordenes Bolivarianas')
# st.subheader('Inventory')

# Display orders related content
# Add functionality to interact with orders data from your API
#  Make a GET request to fetch all orders items
response = requests.get(f'{base_url}/orders')
if response.status_code == 200 and response.json().get('items'):
    orders_data = response.json().get('items', [])
    
    # Convert inventory data to a Pandas DataFrame
    df = pd.DataFrame(orders_data, columns=['id', 'contents', 'subtotal', 'tax', 'total', 'currency', 'client', 'order_date', 'shipping_address', 'status', 'payment_method'])
    st.dataframe(df)
    st.table(orders_data)

else:
    st.write('Failed to fetch inventory items from the API')
# import pandas as pd
# import streamlit as st
# import requests

# # Define the base URL of your API
# base_url = 'http://localhost:8000'  # Update with your API URL

# # Define Streamlit app layout
# st.title('Inventario Socialista')

# # Create a sidebar for user input
# selected_table = st.sidebar.selectbox('Select Table', ['orders', 'inventory', 'inventory2'])

# if st.sidebar.title('Orders'):
#     # Display orders related content
#     st.subheader('Orders')
#     # Add functionality to interact with orders data from your API
#     #  Make a GET request to fetch all orders items
#     response = requests.get(f'{base_url}/orders')
#     if response.status_code == 200:
#         orders_data = response.json().get('items', [])
        
#         # Convert inventory data to a Pandas DataFrame
#         df = pd.DataFrame(orders_data, columns=['id', 'contents', 'subtotal', 'tax', 'total', 'currency', 'client', 'order_date', 'shipping_address', 'status', 'payment_method'])
#         st.dataframe(df)
#         st.table(orders_data)

#     else:
#         st.write('Failed to fetch inventory items from the API')

# if selected_table == 'inventory':
#     # Display inventory related content
#     st.subheader('Inventory')

#     # Make a GET request to fetch all inventory items
#     response = requests.get(f'{base_url}/inventory')
#     if response.status_code == 200:
#         inventory_items = response.json().get('items', [])
        
#         # Display inventory items in a table
#         st.table(inventory_items)
#     else:
#         st.write('Failed to fetch inventory items')

# elif selected_table == 'inventory2':
#     # Display inventory related content
#     st.subheader('Inventory2')

#     # Make a GET request to fetch all inventory items from the API endpoint
#     response = requests.get(f'{base_url}/inventory')
#     if response.status_code == 200:
#         inventory_items = response.json().get('items', [])
        
#         # Convert inventory data to a Pandas DataFrame
#         df = pd.DataFrame(inventory_items, columns=['id', 'brand', 'name', 'size', 'quantity', 'category', 'link'])
#         st.dataframe(df)
#     else:
#         st.write('Failed to fetch inventory items from the API')