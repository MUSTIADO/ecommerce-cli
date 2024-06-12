import logging
from sqlalchemy.orm import Session
from models import User, Product, CartItem, UserRole, Session as DBSession
from auth import register, login, logout, get_current_user  # Importing from auth.py
from orders import place_order, view_orders, cancel_order, update_order_status  # Importing from orders.py

# Set up logging
logging.basicConfig(filename='ecommerce.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Restrict certain actions to admins
def admin_required(func):
    def wrapper(*args, **kwargs):
        user = get_current_user()
        if not user or user.role != UserRole.ADMIN:
            print("Admin access required.")
            return
        return func(*args, **kwargs)
    return wrapper

# Add new product (admin only)
@admin_required
def add_product(name, price):
    try:
        with DBSession() as session:
            product = Product(name=name, price=price)
            session.add(product)
            session.commit()
            print(f"Product '{name}' added successfully with price ${price}.")
            logging.info(f"Product added: {name}, Price: ${price}")
    except Exception as e:
        print("An error occurred while adding the product.")
        logging.error(f"Error adding product: {e}")

# List users (admin only)
@admin_required
def list_users():
    try:
        with DBSession() as session:
            users = session.query(User).all()
            for user in users:
                print(f"User ID: {user.id}, Username: {user.username}, Role: {user.role.value}")
    except Exception as e:
        print("An error occurred while listing users.")
        logging.error(f"Error listing users: {e}")

# Delete user (admin only)
@admin_required
def delete_user(user_id):
    try:
        with DBSession() as session:
            user = session.query(User).filter_by(id=user_id).first()
            if user:
                session.delete(user)
                session.commit()
                logging.info(f"User with ID {user_id} deleted.")
                return True
            else:
                logging.warning(f"User with ID {user_id} not found.")
                return False
    except Exception as e:
        logging.error(f"Error deleting user with ID {user_id}: {e}", exc_info=True)
        return False

# List products
def list_products():
    try:
        with DBSession() as session:
            products = session.query(Product).all()
            for product in products:
                print(f"Product ID: {product.id}, Name: {product.name}, Price: ${product.price}")
    except Exception as e:
        print("An error occurred while listing products.")
        logging.error(f"Error listing products: {e}")

# Add to cart
def add_to_cart(product_id):
    user = get_current_user()
    if not user:
        print("Please login first.")
        return
    try:
        with DBSession() as session:
            product = session.query(Product).filter_by(id=product_id).first()
            if not product:
                print("Product not found.")
                return
            cart_item = CartItem(user_id=user.id, product_id=product.id)
            session.add(cart_item)
            session.commit()
            print(f"Product '{product.name}' added to cart.")
            logging.info(f"Product added to cart: {product.name}, User: {user.username}")
    except Exception as e:
        print("An error occurred while adding to cart.")
        logging.error(f"Error adding to cart: {e}")

# View cart
def view_cart():
    user = get_current_user()
    if not user:
        print("Please login first.")
        return
    try:
        with DBSession() as session:
            cart_items = session.query(CartItem).filter_by(user_id=user.id).all()
            if not cart_items:
                print("Your cart is empty.")
                return
            for item in cart_items:
                product = session.query(Product).filter_by(id=item.product_id).first()
                print(f"Product ID: {product.id}, Name: {product.name}, Price: ${product.price}")
    except Exception as e:
        print("An error occurred while viewing the cart.")
        logging.error(f"Error viewing cart: {e}")