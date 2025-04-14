# backend/routes/analytics.py
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.analytics import Analytics
from app import db

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/sales', methods=['GET'])
@jwt_required()
def sales_report():
    identity = get_jwt_identity()
    if identity['role'] != 'seller':
        return jsonify({'message': 'Unauthorized'}), 403
    report = Analytics.get_sales_report(db.session, identity['id'])
    return jsonify(report), 200