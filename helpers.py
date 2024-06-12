from main import *
from auth import register, login, logout, get_current_user
from models import UserRole, OrderStatus
from orders import place_order, view_orders, cancel_order, update_order_status
def main():
    while True:
        user = get_current_user()

        print("\nChoose an action:")
        print("1. Register")
        print("2. Login")
        print("3. Logout")
        print("4. List Users (Admin Only)")
        print("5. Add Product (Admin Only)")
        print("6. List Products")
        print("7. Add to Cart")
        print("8. View Cart")
        print("9. Place Order")
        print("10. View Orders")
        print("11. Cancel Order")
        print("12. Update Order Status (Admin Only)")
        print("13. Delete User (Admin Only)")
        print("14. Exit")
        
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
            logout()
        elif choice == '4':
            if user and user.role == UserRole.ADMIN:
                list_users()
            else:
                print("Admin access required.")
        elif choice == '5':
            if user and user.role == UserRole.ADMIN:
                name = input("Enter product name: ")
                price = float(input("Enter product price: "))
                add_product(name, price)
            else:
                print("Admin access required.")
        elif choice == '6':
            list_products()
        elif choice == '7':
            product_id = int(input("Enter product ID to add to cart: "))
            add_to_cart(product_id)
        elif choice == '8':
            view_cart()
        elif choice == '9':
            place_order()
        elif choice == '10':
            view_orders()
        elif choice == '11':
            order_id = int(input("Enter order ID to cancel: "))
            cancel_order(order_id)
        elif choice == '12':
            if user and user.role == UserRole.ADMIN:
                order_id = int(input("Enter order ID to update: "))
                status = input("Enter new status (pending, processed, delivered, canceled): ").upper()
                status_enum = OrderStatus[status]
                update_order_status(order_id, status_enum)
            else:
                print("Admin access required.")
        elif choice == '13':
            if user and user.role == UserRole.ADMIN:
                user_id = int(input("Enter user ID to delete: "))
                if delete_user(user_id):
                    print(f"User ID: {user_id} deleted successfully.")
                else:
                    print(f"Failed to delete User ID: {user_id}.")
            else:
                print("Admin access required.")
        elif choice == '14':
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please try again.")

if _name_ == "_main_":
    main()