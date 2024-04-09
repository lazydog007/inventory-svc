import json
import sqlite3
import csv

#  Table creation and population
def create_inventory_table():
  conn = sqlite3.connect('data/database.db')
  cursor = conn.cursor()

  cursor.execute('''
      CREATE TABLE IF NOT EXISTS inventory (
          id INTEGER PRIMARY KEY,
          brand TEXT NOT NULL,
          name TEXT NOT NULL,
          size TEXT,
          quantity INTEGER,
          category TEXT,
          link TEXT
      )
  ''')

  conn.commit()
  print("successfully created inventory table")
  conn.close()

def populate_inventory_table():
    conn = sqlite3.connect('data/database.db')
    cursor = conn.cursor()

    with open('data/mock_inventory_data.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            cursor.execute("INSERT INTO inventory (brand, name, size, quantity, category, link) VALUES (?, ?, ?, ?, ?, ?)", (row[0], row[1], row[2], row[3], row[4], row[5]))

    conn.commit()
    print("successfully populated inventory table")
    conn.close()

# Orders Table
def create_orders_table():
    conn = sqlite3.connect('data/database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contents TEXT NOT NULL,
            pricing JSONB NOT NULL,
            client TEXT NOT NULL,
            phone_number TEXT,
            email TEXT,
            order_date DATETIME,
            shipping_address TEXT,
            status TEXT,
            payment_method TEXT
        )
    ''')

    conn.commit()
    print("successfully created orders table")
    conn.close()

def populate_orders_table():
    conn = sqlite3.connect('data/database.db')
    cursor = conn.cursor()

    with open('data/mock_orders_data.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:

            cursor.execute("INSERT INTO orders (contents, pricing, client, phone_number, email, order_date, shipping_address, status, payment_method) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))

    conn.commit()
    print("successfully populated orders table")
    conn.close()

# ========================== FUNCTIONS ============================
def show_all_table_values(table_name):
    conn = sqlite3.connect('data/database.db')
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table_name}")
    all_rows = cursor.fetchall()

    response = []
    for row in all_rows:
        response.append(row)

    conn.close()
    return response


def search_in_column(table_name, column_name, query):
    conn = sqlite3.connect('data/database.db')
    cursor = conn.cursor()

    if column_name == 'id':
        sql_query = f"SELECT * FROM {table_name} WHERE {column_name} = {query}"
        cursor.execute(sql_query, query)
    else:
        sql_query = f"SELECT * FROM {table_name} WHERE {column_name} LIKE ?"
        cursor.execute(sql_query, ('%' + query + '%',))

    matching_rows = cursor.fetchall()

    response = []
    for row in matching_rows:
        response.append(row)

    conn.close()
    return response

def search_multi_in_column(table_name, column_name, query_list):
    conn = sqlite3.connect('data/database.db')
    cursor = conn.cursor()
    response = []
    for query in query_list:
        if column_name == 'id':
            sql_query = f"SELECT * FROM {table_name} WHERE {column_name} = {query}"
            cursor.execute(sql_query)
        else:
            sql_query = f"SELECT * FROM {table_name} WHERE {column_name} LIKE ?"
            cursor.execute(sql_query, ('%' + query + '%',))

        matching_rows = cursor.fetchall()

        for row in matching_rows:
            response.append(row)

    conn.close()
    return response


def get_specific_orders(order_ids):
    conn = sqlite3.connect('data/database.db')
    cursor = conn.cursor()
    # Create a comma-separated string of order IDs
    order_ids_str = ', '.join(map(str, order_ids))

    # Execute a single query to retrieve orders with the specified IDs
    cursor.execute(f"SELECT * FROM orders WHERE id IN ({order_ids_str})")
    orders = cursor.fetchall()

    # Log missing orders
    found_order_ids = [order[0] for order in orders]
    missing_orders = set(order_ids) - set(found_order_ids)
    for missing_order_id in missing_orders:
        print(f"Order with ID {missing_order_id} not found")

    conn.close()
    return orders

# Inserts new order and returns order id
def insert_order(order_details):
    conn = sqlite3.connect('data/database.db')
    cursor = conn.cursor()

    contents_json = json.dumps(order_details['contents'])  # Convert list to JSON string

    cursor.execute("INSERT INTO orders (contents, pricing, client, phone_number, email, order_date, shipping_address, status, payment_method) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (contents_json, order_details['pricing'], order_details['client'], order_details['order_date'], order_details['shipping_address'], order_details['status'], order_details['payment_method']))

    conn.commit()
    new_order_id = cursor.lastrowid # Returns the ID of the last inserted row
    conn.close()
    return new_order_id

# This updates a speficic row in the order without retrieving everything
def update_order(order_id, updated_details):
    conn = sqlite3.connect('data/database.db')
    cursor = conn.cursor()

    # Build the SQL query dynamically based on the fields provided in updated_details
    set_clause = ", ".join([f"{key} = ?" for key in updated_details.keys()])
    sql_query = f"UPDATE orders SET {set_clause} WHERE id = ?"

    # Prepare the values for the placeholders in the SQL query
    values = list(updated_details.values())
    values.append(order_id)  # Add order_id to the end of values list for the WHERE clause

    cursor.execute(sql_query, values)
    conn.commit()
    conn.close()
    
# This updates a speficic row in the order without retrieving everything
def update_row_by_id(table_name, row_id, updated_details):
    conn = sqlite3.connect('data/database.db')
    cursor = conn.cursor()

    # Build the SQL query dynamically based on the fields provided in updated_details
    set_clause = ", ".join([f"{key} = ?" for key in updated_details.keys()])
    sql_query = f"UPDATE {table_name} SET {set_clause} WHERE id = ?"

    # Prepare the values for the placeholders in the SQL query
    values = list(updated_details.values())
    values.append(row_id)  # Add order_id to the end of values list for the WHERE clause

    cursor.execute(sql_query, values)
    conn.commit()
    conn.close()


# This updates multiple rows at the same time with the same values
def update_rows_by_id(table_name, row_id_list, updated_details):
    conn = sqlite3.connect('data/database.db')
    cursor = conn.cursor()

    # Build the SQL query dynamically based on the fields provided in updated_details
    for row_id in row_id_list:
        set_clause = ", ".join([f"{key} = ?" for key in updated_details.keys()])
        sql_query = f"UPDATE {table_name} SET {set_clause} WHERE id = ?"

        # Prepare the values for the placeholders in the SQL query
        values = list(updated_details.values())
        values.append(row_id)  # Add order_id to the end of values list for the WHERE clause

        cursor.execute(sql_query, values)
        conn.commit()
    conn.close()



# PELIGROSOOOOO

def drop_table(table_name):
    conn = sqlite3.connect('data/database.db')
    cursor = conn.cursor()

    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

    conn.commit()
    print(f"Table {table_name} is dead")
    conn.close()

def drop_all_tables():
    conn = sqlite3.connect('data/database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    for table in tables:
        if table[0] != 'sqlite_sequence':
            cursor.execute(f"DROP TABLE IF EXISTS {table[0]}")

    conn.commit()
    print(f"All Tables are dead")
    conn.close()

def cleanup():
    drop_all_tables()
    create_inventory_table()
    create_orders_table()
    populate_inventory_table()
    populate_orders_table()
    print("Done cleaning")

cleanup()
# populate_orders_table()
