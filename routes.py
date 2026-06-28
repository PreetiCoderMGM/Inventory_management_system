from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from extensions import db
from models import Product

# Define the blueprint
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def dashboard():
    total_products = Product.query.count()
    total_stock = db.session.query(db.func.sum(Product.quantity)).scalar() or 0
    total_value = db.session.query(db.func.sum(Product.quantity * Product.price)).scalar() or 0.0
    low_stock = Product.query.filter(Product.quantity <= 5).count()

    return render_template('dashboard.html',
                           total_products=total_products,
                           total_stock=total_stock,
                           total_value=round(total_value, 2),
                           low_stock=low_stock)


@main_bp.route('/inventory', methods=['GET'])
def inventory():
    products = Product.query.order_by(Product.date_added.desc()).all()
    return render_template('inventory.html', products=products)


@main_bp.route('/inventory/add', methods=['POST'])
def add_product():
    try:
        name = request.form.get('name')
        sku = request.form.get('sku')
        quantity = int(request.form.get('quantity', 0))
        price = float(request.form.get('price', 0.0))

        existing = Product.query.filter_by(sku=sku).first()
        if existing:
            flash(f"SKU '{sku}' already exists!", "error")
            return redirect(url_for('main.inventory'))

        new_product = Product(name=name, sku=sku, quantity=quantity, price=price)
        db.session.add(new_product)
        db.session.commit()
        flash("Product added successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error adding product: {str(e)}", "error")

    return redirect(url_for('main.inventory'))


@main_bp.route('/inventory/update/<int:id>', methods=['POST'])
def update_product(id):
    product = Product.query.get_or_404(id)
    try:
        product.name = request.form.get('name')
        product.quantity = int(request.form.get('quantity', 0))
        product.price = float(request.form.get('price', 0.0))

        db.session.commit()
        flash("Product updated successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error updating product: {str(e)}", "error")

    return redirect(url_for('main.inventory'))


@main_bp.route('/inventory/delete/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"success": True, "message": "Product deleted successfully."})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500