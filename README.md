# E-Commerce Command Line Interface (CLI) Project

## Overview
This project is a command-line interface (CLI) application for managing an e-commerce platform. It allows users to perform various actions such as registering, logging in, listing products, adding products to cart, placing orders, and more, all from the terminal.

## Project Structure
```ecommerce-cli
├── ecommerce
│   ├── database.py
│   ├── log.py
│   ├── main.py
│   ├── models.py
│   ├── utils.py
│
├── Pipfile
├── Pipfile.lock
└── README.md
```

## Features
- User Authentication: Users can register with a username and password, and then log in and log out securely.
- Product Management: Products can be listed, and users can view details and add them to their cart.
- Order Management: Users can place orders, view their order history, and update order status.
- Admin Functionality: Admin users can add new products to the database.

## Objectives
1. Efficiency: Simplify e-commerce management for small businesses.
2. Customization: Allow developers to extend features or integrate the CLI into existing workflows.


## Installation
Clone the repository:[Link to Repository](https://github.com/achoclate/ecommerce-cli)


## Navigate to the project directory: 
cd ecommerce-cli

## Install dependencies:
- pipenv install
- pipenv shell
- pipenv install sqlalchemy


## Usage
Run:python ecommerce/main.py

Follow the prompts to choose an action from the menu and provide any necessary inputs.

For actions that require user input (e.g., registering, logging in, adding products), follow the instructions provided by the CLI.

## Technologies Used
- Python
- SQLite

## Contribution
Contributions are welcome! If you find a bug or have a feature request, please open an issue. Pull requests are also appreciated.

## License 
This project was licensed by :
- Ann Achoki
- Abdifatah Farah
- Mustafa Adan
- Virginia Gichira
- Wilson Gitonga

