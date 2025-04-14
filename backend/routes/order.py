# backend/routes/order.py
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.order import Order
from app import db

order_bp = Blueprint('order', __name__)

@order_bp.route('/list', methods=['GET'])
@jwt_required()
def list_orders():
    identity = get_jwt_identity()
    if identity['role'] != 'seller':
        return jsonify({'message': 'Unauthorized'}), 403
    orders = Order.get_orders(db.session, identity['id'])
    return jsonify([{
        'id': o.id,
        'product_name': o.product.name,
        'quantity': o.quantity,
        'total_price': o.total_price,
        'status': o.status
    } for o in orders]), 200