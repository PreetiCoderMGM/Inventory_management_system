from db_layer import Product


def get_dashboard_metrics():
    try:
        total_products = Product.get_product_count()
        total_stock = Product.get_product_stock()
        total_value = Product.get_total_value()
        low_stock = Product.get_low_stock()
        return {"total_products": total_products, "total_stock": int(total_stock),
                "total_value": round(float(total_value), 2), "low_stock": low_stock}
    except Exception as e:
        print(e)
        return {"total_products": 0, "total_stock": 0, "total_value": 0, "low_stock": 0}


def get_all_products():
    try:
        products = Product.get_all_product()
        return [p.to_dict() for p in products]
    except Exception as e:
        print(e)
        return []


def create_product(data: dict):
    try:
        product = Product.get_by_sku_id(data.get('sku'))
        if product:
            return {"success": False, "message": f"SKU '{data.get('sku')}' already exists!"}
        new_product = Product.add_product(data)
        return {"success": True, "product": new_product.to_dict()}
    except Exception as e:
        print(e)
        return {"success": False, "product": {}}


def update_product(product_id, data):
    try:
        product = Product.get_by_id(product_id)
        if not product:
            return {"success": False, "message": "Product not found"}

        product = product.update_product(data)
        return {"success": True, "product": product.to_dict()}
    except Exception as e:
        print(e)
        return {"success": False, "product": {}}


def delete_product(product_id):
    try:
        product = Product.get_by_id(product_id)
        if not product:
            return {"success": False, "message": "Product not found"}
        product.delete_product()
        return {"success": True, "message": "Product deleted successfully."}
    except Exception as e:
        print(e)
        return {"success": False, "message": "Unable to delete product."}