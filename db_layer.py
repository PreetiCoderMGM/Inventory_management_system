from extensions import db
from datetime import datetime
import config


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    quantity = db.Column(db.Integer, default=0, nullable=False)
    price = db.Column(db.Float, default=0.0, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "sku": self.sku, "quantity": self.quantity, "price": self.price}

    @staticmethod
    def add_product(data):
        new_product = Product(name=data.get('name'), sku=data.get('sku'), quantity=int(data.get('quantity', 0)),
                              price=float(data.get('price', 0.0)))
        db.session.add(new_product)
        db.session.commit()
        return new_product

    @staticmethod
    def get_product_count():
        return Product.query.count()

    @staticmethod
    def get_product_stock():
        return db.session.query(db.func.sum(Product.quantity)).scalar() or 0

    @staticmethod
    def get_total_value():
        return db.session.query(db.func.sum(Product.quantity * Product.price)).scalar() or 0.0

    @staticmethod
    def get_low_stock():
        return Product.query.filter(Product.quantity <= config.LOW_STOCK_THRESHOLD).count()

    @staticmethod
    def get_all_product():
        return Product.query.order_by(Product.date_added.desc()).all()

    @staticmethod
    def get_by_sku_id(sku_id):
        return Product.query.filter_by(sku=sku_id).first()

    @staticmethod
    def get_by_id(product_id):
        return Product.query.get(product_id)

    def update_product(self, data):
        self.name = data.get('name', self.name)
        self.quantity = int(data.get('quantity', self.quantity))
        self.price = float(data.get('price', self.price))
        db.session.commit()
        return self

    def delete_product(self):
        db.session.delete(self)
        db.session.commit()
        return True
