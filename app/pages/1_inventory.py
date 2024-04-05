# Display inventory related content
import requests
import streamlit as st
# Define the base URL of your API
base_url = 'http://localhost:8000'  # Update with your API URL

# Define Streamlit app layout
st.title('Inventario Socialista')
# st.subheader('Inventory')

# Make a GET request to fetch all inventory items
response = requests.get(f'{base_url}/inventory')
if response.status_code == 200:
    inventory_items = response.json().get('items', [])
    
    # Display inventory items in a table
    st.table(inventory_items)
else:
    st.write('Failed to fetch inventory items')