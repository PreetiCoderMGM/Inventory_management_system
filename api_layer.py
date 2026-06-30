from flask import Blueprint, request, jsonify
import bl_layer

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/metrics', methods=['GET'])
def metrics():
    data = bl_layer.get_dashboard_metrics()
    return jsonify(data)


@api_bp.route('/products', methods=['GET'])
def get_products():
    data = bl_layer.get_all_products()
    return jsonify(data)


@api_bp.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    result = bl_layer.create_product(data)
    if result['success']:
        return jsonify(result), 201
    return jsonify(result), 400


@api_bp.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    result = bl_layer.update_product(id, data)
    if result['success']:
        return jsonify(result), 200
    return jsonify(result), 400


@api_bp.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    result = bl_layer.delete_product(id)
    if result['success']:
        return jsonify(result), 200
    return jsonify(result), 404
