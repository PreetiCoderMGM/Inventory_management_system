from flask import Blueprint, request, jsonify
import bl_layer

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/metrics', methods=['GET'])
def metrics():
    try:
        data = bl_layer.get_dashboard_metrics()
        return jsonify(data)
    except Exception as ex:
        print(f"Request failed. Reason: Exception: {ex}.")
        return jsonify({"success": False, "message": "Internal server error."}), 500


@api_bp.route('/products', methods=['GET'])
def get_products():
    try:
        data = bl_layer.get_all_products()
        return jsonify(data)
    except Exception as ex:
        print(f"Request failed. Reason: Exception: {ex}.")
        return jsonify({"success": False, "message": "Internal server error."}), 500


@api_bp.route('/products', methods=['POST'])
def add_product():
    try:
        data = request.get_json()
        result = bl_layer.create_product(data)
        if result['success']:
            return jsonify(result), 201
        return jsonify(result), 400
    except Exception as ex:
        print(f"Request failed. Reason: Exception: {ex}.")
        return jsonify({"success": False, "message": "Internal server error."}), 500


@api_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id: int):
    try:
        data = request.get_json()
        result = bl_layer.update_product(product_id, data)
        if result['success']:
            return jsonify(result), 200
        return jsonify(result), 400
    except Exception as ex:
        print(f"Request failed. Reason: Exception: {ex}.")
        return jsonify({"success": False, "message": "Internal server error."}), 500


@api_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id: int):
    try:
        result = bl_layer.delete_product(product_id)
        if result['success']:
            return jsonify(result), 200
        return jsonify(result), 404
    except Exception as ex:
        print(f"Request failed. Reason: Exception: {ex}.")
        return jsonify({"success": False, "message": "Internal server error."}), 500
