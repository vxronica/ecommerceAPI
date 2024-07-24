### E-commerce Application

This is an E-Commerce API built with Flask, SQLAlchemy, and Marshmallow. The application allows for the management of customers, customer accounts, products, and orders. It provides endpoints to perform CRUD (Create, Read, Update, Delete) operations on these entities.

## Features

1. **Customer and CustomerAccount Management**:
    - Create, Read, Update, Delete endpoints for managing Customers.
    - Create, Read, Update, Delete endpoints for managing CustomerAccounts.

2. **Product Catalog**:
    - Create, Read, Update, Delete endpoints for managing Products.
    - List all available products.

3. **Order Processing**:
    - Place, Retrieve, and Update orders.
    - Track and manage order history.

4. **Database Integration**:
    - Utilizes Flask-SQLAlchemy to integrate with a MySQL database.
    - Proper relationships established between tables.

5. **Data Validation and Error Handling**:
    - Data validation using Marshmallow.
    - Error handling with informative messages.

## Getting Started

### Prerequisites

- Python 3.7+
- MySQL Database

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/vxronica/ecommerceAPI.git
    cd ecommerceAPI
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv myvenv
    source myvenv/bin/activate
    ```
3. **Install required packages:**
   ```bash
   pip install flask flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy
   ```

4. **Configure the database:**
   Update the `SQLALCHEMY_DATABASE_URI` in `app.py` to match your MySQL database credentials:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:you_password@localhost/e_commerce_db'
   ```

5. **Initialize the database:**
   ```bash
   python app.py
   ```

## API Endpoints

### Customer 

- **GET /customers**: Retrieve all customers
- **POST /customers**: Add a new customer
- **PUT /customers/<id>**: Update a customer's details
- **DELETE /customers/<id>**: Delete a customer

### CustomerAccount

- **GET /accounts**: Retrieve all customer accounts
- **POST /accounts**: Add a new customer account
- **PUT /accounts/<id>**: Update a customer account's details
- **DELETE /accounts/<id>**: Delete a customer account

### Product

- **GET /products**: Retrieve all products
- **POST /products**: Add a new product
- **PUT /products/<id>**: Update a product's details
- **DELETE /products/<id>**: Delete a product

### Order

- **GET /orders**: Retrieve all orders
- **POST /orders**: Place a new order
- **PUT /orders/<id>**: Update an order's details
- **DELETE /orders/<id>**: Delete an order

## Database Tables

### Customer

- **id**: Integer, Primary Key
- **name**: String(255), Not Null
- **email**: String(320)
- **phone**: String(15)

### CustomerAccount

- **id**: Integer, Primary Key
- **username**: String(255), Unique, Not Null
- **password**: String(255), Not Null
- **customer_id**: Integer, Foreign Key to Customer

### Product

- **id**: Integer, Primary Key
- **name**: String(255)
- **price**: Float, Not Null

### Order

- **id**: Integer, Primary Key
- **date**: Date, Not Null
- **customer_id**: Integer, Foreign Key to Customer


# github link: https://github.com/vxronica/ecommerceAPI
