from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
from marshmallow import ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:your_password@localhost/ecommerceAPI'
db = SQLAlchemy(app)
ma = Marshmallow(app)

#Customer Schema
class CustomerSchema(ma.Schema):
    name = fields.String(required=True)
    email = fields.String(required=True)
    phone = fields.String(required=True)

    class Meta:
        fields = ("name", "email", "phone", "id")

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

#Customer Table
class Customer(db.Model):
    __tablename__ = 'Customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(320))
    phone= db.Column(db.String(15))
    orders = db.relationship("Order", backref='customer') 

#Order Table
class Order(db.Model):
    __tablename__ = 'Orders'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customers.id'))
    products = db.relationship("Product",secondary=order_product, backref=db.backref('orders'))

#CustomerAccount Table
class CustomerAccount(db.Model):
    __tablename__ = 'Customer_Accounts'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customers.id'))
    customer = db.relationship('Customer', backref='customer_account', uselist=False)

#Order-Product Association Table
order_product = db.Table('Order_Product',
        db.Column('order_id', db.Integer, db.ForeignKey('Orders.id'), primary_key=True),
        db.Column('product_id', db.Integer, db.ForeignKey('Products.id'), primary_key=True)
)

#Product Table
class Product(db.Model):
    __tablename__ = 'Products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=False)
    orders = db.relationship("Order", secondary=order_product, backref=db.backref('products'))

#CustomerAccount Schema
class CustomerAccountSchema(ma.Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    customer_id = fields.Integer(required=True)

    class Meta:
        fields = ("username", "password", "customer_id", "id")

account_schema = CustomerAccountSchema()
accounts_schema = CustomerAccountSchema(many=True)

#Product Schema
class ProductSchema(ma.Schema):
    name = fields.String(required=True)
    price = fields.Float(required=True)

    class Meta:
        fields = ("name", "price", "id")

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

#Order Schema
class OrderSchema(ma.Schema):
    date = fields.Date(required=True)
    customer_id = fields.Integer(required=True)
    products = fields.List(fields.Integer(), required=True)

    class Meta:
        fields = ("date", "customer_id", "products", "id")

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)


#Retrieves all customers
@app.route('/customers', methods=["GET"])
def get_customers():
    customers = Customer.query.all()
    return customers_schema.jsonify(customers)

#Add a new customer
@app.route('/customers', methods=["POST"])
def add_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_customer = Customer(name=customer_data['name'], email=customer_data['email'], phone=customer_data['phone'])
    db.session.add(new_customer)
    db.session.commit()

#Updates customer details
@app.route("/customers/<int:id>", methods=["PUT"])
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    customer.name = customer_data['name']
    customer.email = customer_data['email']
    customer.phone = customer_data['phone']
    db.session.commit()
    return jsonify({"message": "Updated the customer successfully"}), 200

#Deletes customer
@app.route("/customers/<int:id>", methods=["DELETE"])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer removed successfully"}), 200

#Retrieves all customer accounts
@app.route('/accounts', methods=["GET"])
def get_accounts():
    accounts = CustomerAccount.query.all()
    return accounts_schema.jsonify(accounts)

#Adds a new customer account
@app.route('/accounts', methods=["POST"])
def add_account():
    try:
        account_data = account_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_account = CustomerAccount(username=account_data['username'], password=account_data['password'], customer_id=account_data['customer_id'])
    db.session.add(new_account)
    db.session.commit()

#Updates customer Account Details
@app.route("/accounts/<int:id>", methods=["PUT"])
def update_account(id):
    account = CustomerAccount.query.get_or_404(id)
    try:
        account_data = account_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    account.username = account_data['username']
    account.password = account_data['password']
    db.session.commit()
    return jsonify({"message": "Updated the account successfully"}), 200

#Deletes customer account by id
@app.route("/accounts/<int:id>", methods=["DELETE"])
def delete_account(id):
    account = CustomerAccount.query.get_or_404(id)
    db.session.delete(account)
    db.session.commit()
    return jsonify({"message": "Account removed successfully"}), 200

#Gets all products
@app.route('/products', methods=["GET"])
def get_products():
    products = Product.query.all()
    return products_schema.jsonify(products)

#Adds a new product
@app.route('/products', methods=["POST"])
def add_product():
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_product = Product(name=product_data['name'], price=product_data['price'])
    db.session.add(new_product)
    db.session.commit()

#Updates product details
@app.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    product = Product.query.get_or_404(id)
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    product.name = product_data['name']
    product.price = product_data['price']
    db.session.commit()
    return jsonify({"message": "Updated the product successfully"}), 200

#Deeletes product 
@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product removed successfully"}), 200

#gets all orders
@app.route('/orders', methods=["GET"])
def get_orders():
    orders = Order.query.all()
    return orders_schema.jsonify(orders)

#places a new order
@app.route('/orders', methods=["POST"])
def place_order():
    try:
        order_data = order_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_order = Order(date=order_data['date'], customer_id=order_data['customer_id'])
    for product_id in order_data['products']:
        product = Product.query.get(product_id)
        if product:
            new_order.products.append(product)
    db.session.add(new_order)
    db.session.commit()
    return order_schema.jsonify(new_order), 200

#updates order details
@app.route("/orders/<int:id>", methods=["PUT"])
def update_order(id):
    order = Order.query.get_or_404(id)
    try:
        order_data = order_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    order.date = order_data['date']
    order.customer_id = order_data['customer_id']
    order.products = []
    for product_id in order_data['products']:
        product = Product.query.get(product_id)
        if product:
            order.products.append(product)
    db.session.commit()
    return jsonify({"message": "Updated the order successfully"}), 200

#deletes order
@app.route("/orders/<int:id>", methods=["DELETE"])
def delete_order(id):
    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Order removed successfully"}), 200

#initialize the database and create tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
