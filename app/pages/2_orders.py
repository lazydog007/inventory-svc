# Display orders related content
import pandas as pd
# import requests
import streamlit as st

from database import search_multi_in_column, show_all_table_values, update_rows_by_id # note: its not app.database because home.py is inside /app
TABLE_NAME = "orders"
st.set_page_config(
    page_title="Orders Socialista",
    page_icon=":bar-chart",
    # initial_sidebar_state='collapsed',
    layout="wide"
)

st.title('Orders Socialista')

col1, col2, col3, col4 = st.columns(4)
with col1:  
    show_search = st.checkbox("Search", value=True)

with col2:
    show_all_orders_table = st.checkbox("All Orders")

with col3:
    show_update_form = st.checkbox("Update")

with col4:
    show_create_form = st.checkbox("Create")

col11, col22, = st.columns(2)

if show_search:
    with col11:
        with st.form("search_form"):
            st.subheader("Search")
            selected_column = st.selectbox("Select column to search in", ['id', 'phone_number', 'email', 'client', 'order_date', 'shipping_address', 'status', 'payment_method'], index=7)
            query_terms = st.text_input("Enter search terms separated by commas. ex. 1, 2, 3, 4")
            query_term_list = [term.strip() for term in query_terms.split(',')]
            
            if st.form_submit_button("Search"):
                st.experimental_rerun()
    try:
        if query_term_list and query_term_list != ['']:
            st.subheader('Search Results')
            search_results = []
            search_results.extend(search_multi_in_column("orders", selected_column, query_term_list))
            if search_results:
                df = pd.DataFrame(search_results, columns=['id', 'contents', 'pricing', 'client', 'phone_number', 'email','order_date', 'shipping_address', 'status', 'payment_method'])
                st.dataframe(df)
            else:
                st.write("No results found")
    except Exception as e:
        print(f"Exception: {e}")
        st.write("Nothing found")

with col22:
    if show_update_form:
        with st.form("update_form"):
            st.subheader("Update Orders Row")
            product_ids = st.text_input("Enter search terms separated by commas. ex. 1, 2, 3, 4")
            product_id_list = [term.strip() for term in product_ids.split(',')]
            
            col1, col2 = st.columns(2)

            with col1:
                updated_brand = st.text_input("Enter updated brand")
                updated_name = st.text_input("Enter updated name")
                updated_size = st.text_input("Enter updated size")

            with col2:
                updated_quantity = st.text_input("Enter updated quantity")
                updated_category = st.text_input("Enter updated category")
                updated_link = st.text_input("Enter updated link")

            if st.form_submit_button("Update"):
                if product_id_list:
                    updated_values = {
                        'brand': updated_brand,
                        'name': updated_name,
                        'size': updated_size,
                        'quantity': updated_quantity,
                        'category': updated_category,
                        'link': updated_link
                    }

                    filtered_values = {key: value for key, value in updated_values.items() if value != ''}

                    if filtered_values.get('quantity'):
                        filtered_values['quantity'] = int(updated_values['quantity'])

                    update_rows_by_id(TABLE_NAME, product_ids, filtered_values)
                    st.write(f"update value {filtered_values}")

                    if show_search:
                        st.rerun()
                else:
                    st.warning(f"No ID provided")
if show_all_orders_table:
    st.subheader('Orders')
    orders_items = show_all_table_values("orders")

    if orders_items:
        # Convert orders data to a Pandas DataFrame
        df = pd.DataFrame(orders_items, columns=['id', 'contents', 'pricing', 'client', 'phone_number', 'email', 'order_date', 'shipping_address', 'status', 'payment_method'])
        st.dataframe(df)
    else:
        st.write('Nothing in it :(')
