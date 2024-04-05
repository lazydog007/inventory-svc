# Display inventory related content
import pandas as pd
import requests
import streamlit as st
# Define the base URL of your API
base_url = 'http://localhost:8000'  # Update with your API URL

# Define Streamlit app layout
st.title('Inventario Socialista')
# st.subheader('Inventory')

# Make a GET request to fetch all inventory items from the API endpoint
response = requests.get(f'{base_url}/inventory')
if response.status_code == 200:
    inventory_items = response.json().get('items', [])
    
    # Convert inventory data to a Pandas DataFrame
    df = pd.DataFrame(inventory_items, columns=['id', 'brand', 'name', 'size', 'quantity', 'category', 'link'])
    st.dataframe(df)
else:
    st.write('Failed to fetch inventory items from the API')