# backend/routes/product.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.product import Product
from app import db

product_bp = Blueprint('product', __name__)

@product_bp.route('/add', methods=['POST'])
@jwt_required()
def add_product():
    identity = get_jwt_identity()
    if identity['role'] != 'seller':
        return jsonify({'message': 'Unauthorized'}), 403
    data = request.get_json()
    if Product.add_product(
        db.session, identity['id'], data['name'], data['description'], data['price'], data['stock']
    ):
        return jsonify({'message': 'Product added'}), 201
    return jsonify({'message': 'Failed to add product'}), 400

@product_bp.route('/list', methods=['GET'])
@jwt_required()
def list_products():
    identity = get_jwt_identity()
    if identity['role'] != 'seller':
        return jsonify({'message': 'Unauthorized'}), 403
    products = Product.get_products(db.session, identity['id'])
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'price': p.price,
        'stock': p.stock
    } for p in products]), 200

@product_bp.route('/update/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    identity = get_jwt_identity()
    if identity['role'] != 'seller':
        return jsonify({'message': 'Unauthorized'}), 403
    data = request.get_json()
    if Product.update_product(
        db.session, product_id, data['name'], data['description'], data['price'], data['stock']
    ):
        return jsonify({'message': 'Product updated'}), 200
    return jsonify({'message': 'Failed to update product'}), 400

@product_bp.route('/delete/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    identity = get_jwt_identity()
    if identity['role'] != 'seller':
        return jsonify({'message': 'Unauthorized'}), 403
    if Product.delete_product(db.session, product_id):
        return jsonify({'message': 'Product deleted'}), 200
    return jsonify({'message': 'Failed to delete product'}), 400