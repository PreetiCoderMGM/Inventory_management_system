from extensions import db
from db_layer import Product


def get_dashboard_metrics():
    total_products = Product.query.count()
    total_stock = db.session.query(db.func.sum(Product.quantity)).scalar() or 0
    total_value = db.session.query(db.func.sum(Product.quantity * Product.price)).scalar() or 0.0
    low_stock = Product.query.filter(Product.quantity <= 5).count()

    return {
        "total_products": total_products,
        "total_stock": int(total_stock),
        "total_value": round(float(total_value), 2),
        "low_stock": low_stock
    }


def get_all_products():
    products = Product.query.order_by(Product.date_added.desc()).all()
    return [p.to_dict() for p in products]


def create_product(data):
    if Product.query.filter_by(sku=data.get('sku')).first():
        return {"success": False, "message": f"SKU '{data.get('sku')}' already exists!"}

    new_product = Product(
        name=data.get('name'),
        sku=data.get('sku'),
        quantity=int(data.get('quantity', 0)),
        price=float(data.get('price', 0.0))
    )
    db.session.add(new_product)
    db.session.commit()
    return {"success": True, "product": new_product.to_dict()}


def update_product(product_id, data):
    product = Product.query.get(product_id)
    if not product:
        return {"success": False, "message": "Product not found"}

    product.name = data.get('name', product.name)
    product.quantity = int(data.get('quantity', product.quantity))
    product.price = float(data.get('price', product.price))
    db.session.commit()
    return {"success": True, "product": product.to_dict()}


def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return {"success": False, "message": "Product not found"}

    db.session.delete(product)
    db.session.commit()
    return {"success": True, "message": "Product deleted successfully."}