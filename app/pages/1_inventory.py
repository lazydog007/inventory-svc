# Display inventory related content
import pandas as pd
# import requests
import streamlit as st

from database import search_in_column, search_multi_in_column, show_all_table_values # note: its not app.database because home.py is inside /app


st.title('Inventario Socialista')


# st.sidebar.title("Search Inventory")
# selected_column = st.sidebar.selectbox("Select column to search in", ['id', 'brand', 'name', 'size', 'quantity', 'category', 'link'], index=0)
# query_term = st.sidebar.text_input("Enter search term")
# show_results_table = st.sidebar.checkbox("Results Table", value=True)
# show_all_inventory_table = st.sidebar.checkbox("All Inventory")

selected_column = st.selectbox("Select column to search in", ['id', 'brand', 'name', 'size', 'quantity', 'category', 'link'], index=0)
query_terms = st.text_input("Enter search terms separated by commas. ex. 1, 2, 3, 4")
query_term_list = [term.strip() for term in query_terms.split(',')]
show_results_table = st.checkbox("Results Table", value=True)
show_all_inventory_table = st.checkbox("All Inventory")

# Replace or add after the existing code for displaying inventory items
try:
    if query_term_list and query_term_list != [''] and show_results_table:
        st.subheader('Search Results')
        search_results = []
        search_results.extend(search_multi_in_column("inventory", selected_column, query_term_list))
        print("\n")
        print(f"search_results {search_results}")
        print("\n")
        if search_results:
            df = pd.DataFrame(search_results, columns=['id', 'brand', 'name', 'size', 'quantity', 'category', 'link'])
            st.dataframe(df)
        else:
            st.write("No results found")
except Exception as e:
    print(f"Exception: {e}")
    st.write("Nothing found")


if show_all_inventory_table:
    st.subheader('Inventory')
    inventory_items = show_all_table_values("inventory")

    if inventory_items:
        # Convert inventory data to a Pandas DataFrame
        df = pd.DataFrame(inventory_items, columns=['id', 'brand', 'name', 'size', 'quantity', 'category', 'link'])
        st.dataframe(df)
    else:
        st.write('Nothing in it :(')