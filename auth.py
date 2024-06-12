import logging
from sqlalchemy.orm import Session
from models import User, UserRole, Session as DBSession

# Set up logging
logging.basicConfig(filename='ecommerce.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Register user
def register(username, password, role=UserRole.USER):
    try:
        with DBSession() as session:
            if session.query(User).filter_by(username=username).first():
                print("Username already exists.")
                return
            user = User(username=username, password=password, role=role)
            session.add(user)
            session.commit()
            print("User registered successfully.")
            logging.info(f"User registered: {username} as {role.value}")
    except Exception as e:
        print("An error occurred while registering the user.")
        logging.error(f"Error registering user: {e}")

# Login user
def login(username, password):
    try:
        with DBSession() as session:
            user = session.query(User).filter_by(username=username, password=password).first()
            if user:
                with open('session.txt', 'w') as file:
                    file.write(f"{username},{user.role.value}")
                print("Logged in successfully.")
                logging.info(f"User logged in: {username}")
                if user.role == UserRole.ADMIN:
                    print("Welcome Admin!")
                else:
                    print("Welcome User!")
            else:
                print("Invalid username or password.")
    except Exception as e:
        print("An error occurred while logging in.")
        logging.error(f"Error logging in user: {e}")

# Logout user
def logout():
    try:
        with open('session.txt', 'w') as file:
            file.write('')
        print("Logged out successfully.")
        logging.info("User logged out.")
    except Exception as e:
        print("An error occurred while logging out.")
        logging.error(f"Error logging out user: {e}")

# Get current user
def get_current_user():
    try:
        with open('session.txt', 'r') as file:
            data = file.read().strip().split(',')
        if not data or len(data) != 2:
            return None
        username, role = data
        with DBSession() as session:
            return session.query(User).filter_by(username=username, role=UserRole(role)).first()
    except Exception as e:
        logging.error(f"Error getting current user: {e}")
        return None