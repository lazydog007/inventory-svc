from datetime import datetime
from flask import Blueprint, request, jsonify

from app.database import get_specific_orders, insert_order, search_in_column, show_all_table_values, update_order

inventory_blueprint = Blueprint("inventory", __name__)

@inventory_blueprint.route("/health", methods=["GET"])
def health():
    return {"status": "I'm ok Morty"}

# generic, we can search any table for any row
# ex. /search?table=orders&col=id&query=123456
@inventory_blueprint.route("/search", methods=["GET"])
def search_column():
    table = request.args.get('table')
    col = request.args.get('col')
    search_term = request.args.get('query')
    return search_in_column(table, col, search_term)


@inventory_blueprint.route("/<table_name>", methods=["GET"])
def get_all_table_items(table_name):
    all_items = show_all_table_values(table_name)
    return jsonify({"items": all_items})

# ===================== ORDERS ============================
@inventory_blueprint.route("/orders/by_id", methods=["POST"])
def get_orders_by_id():
    order_ids = request.get_json().get('order_ids', [])
    orders = get_specific_orders(order_ids)
    return jsonify({"orders": orders})

# Creates order and stores in database  
@inventory_blueprint.route("/orders/create", methods=["POST"])
def order_create():
    current_order = request.get_json()
    current_order['order_date'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    new_order_id = insert_order(current_order)  # Modify insert_order to return the last inserted ID
    return jsonify({"status": f"Order {new_order_id} created successfully"})

@inventory_blueprint.route("/orders/update/<order_id>", methods=["PUT"])
def order_update(order_id):
    updated_order = request.get_json()  # Assuming the updated order details are sent in JSON format
    
    # Remove 'order_id' from updated_order if it's accidentally included
    updated_order.pop('order_id', None)

    update_order(order_id, updated_order)
    return jsonify({"status": f"Order {order_id} updated successfully"})
