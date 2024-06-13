from utils import *

# Function to view all orders for admin
def view_all_orders():
    try:
        with Session() as session:
            orders = session.query(Order).all()
            if not orders:
                print("No orders found.")
            else:
                for order in orders:
                    print(f"Order ID: {order.id}")
                    print(f"User: {order.user.username}")
                    print(f"Products: {[item.product.name for item in order.order_items]}")
                    print(f"Total Price: {order.total}")
                    print(f"Status: {order.status.value}")
    except Exception as e:
        print("An error occurred while viewing all orders.")
        logging.error(f"Error viewing all orders: {e}")

# Main program
def main():
    while True:
        user = get_current_user()

        if not user:
            print("\nChoose an action:")
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                username = input("Enter username: ")
                password = input("Enter password: ")
                role_input = input("Enter role (user/admin): ").strip().lower()
                role = UserRole.ADMIN if role_input == "admin" else UserRole.USER
                register(username, password, role)
            elif choice == '2':
                username = input("Enter username: ")
                password = input("Enter password: ")
                login(username, password)
            elif choice == '3':
                print("Exiting program. Goodbye!")
                break
            else:
                print("Invalid choice. Please choose again.")
        else:
            if user.role == UserRole.ADMIN:
                print("\nAdmin Menu:")
                print("1. Logout")
                print("2. List Users")
                print("3. Add Product")
                print("4. List Products")
                print("5. View all orders")
                print("6. Update Order Status")
                print("7. Delete User")
                print("8. Exit")
            else:
                print("\nUser Menu:")
                print("1. Logout")
                print("2. List Products")
                print("3. Add to Cart")
                print("4. Empty Cart")
                print("5. View Cart")
                print("6. Place Order")
                print("7. View Orders")
                print("8. Cancel Order")
                print("9. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                logout()
            elif choice == '2':
                if user.role == UserRole.ADMIN:
                    list_users()
                else:
                    list_products()
            elif choice == '3':
                if user.role == UserRole.ADMIN:
                    name = input("Enter product name: ")
                    price = float(input("Enter product price: "))
                    add_product(name, price)
                else:
                    product_id = int(input("Enter product ID to add to cart: "))
                    add_to_cart(product_id)
            elif choice == '4':
                if user.role == UserRole.ADMIN:
                    list_products()
                else:
                    empty_cart()
            elif choice == '5':
                if user.role == UserRole.ADMIN:
                    view_all_orders()  # View all orders for admin
                else:
                    view_cart()
            elif choice == '6':
                if user.role == UserRole.ADMIN:
                    order_id = int(input("Enter order ID to update status: "))
                    status_input = input("Enter new status (pending/processed/delivered/canceled): ").strip().lower()
                    status = {
                        'pending': OrderStatus.PENDING,
                        'processed': OrderStatus.PROCESSED,
                        'delivered': OrderStatus.DELIVERED,
                        'canceled': OrderStatus.CANCELED
                    }.get(status_input)

                    if status:
                        update_order_status(order_id, status)
                    else:
                        print("Invalid status input.")
                else:
                    place_order()
            elif choice == '7':
                if user.role == UserRole.ADMIN:
                    username = input("Enter username to delete: ")
                    delete_user(username)
                else:
                    view_orders()
            elif choice == '8':
                if user.role == UserRole.ADMIN:
                    print("Exiting program. Goodbye!")
                    break
                else:
                    order_id = int(input("Enter order ID to cancel: "))
                    cancel_order(order_id)
            elif choice == '9' and user.role == UserRole.USER:
                print("Exiting program. Goodbye!")
                break
            else:
                print("Invalid choice. Please choose again.")

if __name__ == "__main__":
    main()
