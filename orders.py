import logging
from sqlalchemy.orm import Session
from models import User, Product, CartItem, Order, OrderItem, OrderStatus, UserRole, Session as DBSession
from auth import get_current_user  # Importing from auth.py

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

# Place order
def place_order():
    user = get_current_user()
    if not user:
        print("Please login first.")
        return

    try:
        with DBSession() as session:
            cart_items = session.query(CartItem).filter_by(user_id=user.id).all()
            if not cart_items:
                print("Your cart is empty. Please add items to your cart before placing an order.")
                return

            total = 0
            order_items = []
            for item in cart_items:
                product = session.query(Product).filter_by(id=item.product_id).first()
                total += product.price
                order_items.append(OrderItem(product_id=product.id, quantity=1, unit_price=product.price))

            order = Order(user_id=user.id, total=total, status=OrderStatus.PENDING)
            order.order_items = order_items
            session.add(order)
            session.commit()

            # Remove items from the cart after placing the order
            session.query(CartItem).filter_by(user_id=user.id).delete()
            
            print("Order placed successfully.")
            logging.info(f"Order placed: {order.id}, User: {user.username}")

    except Exception as e:
        print("An error occurred while placing the order.")
        logging.error(f"Error placing order: {e}")

# View orders
def view_orders():
    user = get_current_user()
    if not user:
        print("Please login first.")
        return
    try:
        with DBSession() as session:
            orders = session.query(Order).filter_by(user_id=user.id).all()
            if not orders:
                print("You have no orders.")
                return
            for order in orders:
                print(f"Order ID: {order.id}, Status: {order.status.value}")
                order_items = session.query(OrderItem).filter_by(order_id=order.id).all()
                for item in order_items:
                    product = session.query(Product).filter_by(id=item.product_id).first()
                    print(f"  Product ID: {product.id}, Name: {product.name}, Price: ${product.price}, Quantity: {item.quantity}")
    except Exception as e:
        print("An error occurred while viewing orders.")
        logging.error(f"Error viewing orders: {e}")

# Cancel order
def cancel_order(order_id):
    user = get_current_user()
    if not user:
        print("Please login first.")
        return
    try:
        with DBSession() as session:
            order = session.query(Order).filter_by(id=order_id, user_id=user.id).first()
            if not order:
                print("Order not found.")
                return
            if order.status != OrderStatus.PENDING:
                print("Only pending orders can be canceled.")
                return
            order.status = OrderStatus.CANCELED
            session.commit()
            print("Order canceled successfully.")
            logging.info(f"Order canceled: {order_id}, User: {user.username}")
    except Exception as e:
        print("An error occurred while canceling the order.")
        logging.error(f"Error canceling order: {e}")

# Update order status (admin only)
@admin_required
def update_order_status(order_id, status):
    try:
        with DBSession() as session:
            order = session.query(Order).filter_by(id=order_id).first()
            if not order:
                print("Order not found.")
                return
            order.status = status
            session.commit()
            print(f"Order status updated to {status.value}.")
            logging.info(f"Order status updated: {order_id}, Status: {status.value}")
    except Exception as e:
        print("An error occurred while updating the order status.")
        logging.error(f"Error updating order status: {e}")