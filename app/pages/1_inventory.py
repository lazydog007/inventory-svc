# Display inventory related content
import pandas as pd
# import requests
import streamlit as st

from database import search_in_column, search_multi_in_column, show_all_table_values, update_row_by_id # note: its not app.database because home.py is inside /app
TABLE_NAME = "inventory"
st.set_page_config(
    page_title="Inventorio Socialista",
    page_icon=":bar-chart",
    initial_sidebar_state='collapsed',
    layout="wide"
)

st.title('Inventario Socialista')


# show_results_table = st.checkbox("Results Table", value=True)
show_search = st.checkbox("Search", value=True)
show_all_inventory_table = st.checkbox("All Inventory")
show_update_form = st.checkbox("Update")

# Replace or add after the existing code for displaying inventory items
if show_search:
    with st.form("search_form"):
        selected_column = st.selectbox("Select column to search in", ['id', 'brand', 'name', 'size', 'quantity', 'category', 'link'], index=0)
        query_terms = st.text_input("Enter search terms separated by commas. ex. 1, 2, 3, 4")
        query_term_list = [term.strip() for term in query_terms.split(',')]
        
        if st.form_submit_button("Search"):
            st.experimental_rerun()
    try:
        if query_term_list and query_term_list != ['']:
            st.subheader('Search Results')
            search_results = []
            search_results.extend(search_multi_in_column("inventory", selected_column, query_term_list))
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

if show_update_form:
    with st.form("update_form"):
        st.subheader("Update Inventory Row")
        product_id = st.text_input("Enter product id")
        updated_brand = st.text_input("Enter updated brand")
        updated_name = st.text_input("Enter updated name")
        updated_size = st.text_input("Enter updated size")
        # updated_quantity = st.number_input("Enter updated quantity", min_value=0)
        updated_quantity = st.text_input("Enter updated quantity")
        updated_category = st.text_input("Enter updated category")
        updated_link = st.text_input("Enter updated link")

        if st.form_submit_button("Update"):
            if product_id:
                updated_values = {
                    'brand': updated_brand,
                    'name': updated_name,
                    'size': updated_size,
                    'quantity': int(updated_quantity),
                    'category': updated_category,
                    'link': updated_link
                }

                filtered_values = {key: value for key, value in updated_values.items() if value != ''}

                update_row_by_id(TABLE_NAME, product_id, filtered_values)
                st.write(f"update value {filtered_values}")

                if show_search:
                    st.experimental_rerun()
            else:
                st.warning(f"No ID provided")