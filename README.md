# :hearts: LiaShopStar - An online store
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.1-green.svg)](https://djangoproject.com)
[![License](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)

:page_with_curl: LiaShopStar is an online store that is designed to practice and simulate buying and selling processes on the Internet.
This project allows users to have a real online shopping experience and developers can use it to improve their programming and web design skills.

## Project goals:
- Simulation of online shopping: users can view and buy different products.
- Learning web development concepts: This project is a good opportunity to learn and practice key concepts in web development and programming.
- Interaction with the database: Management of products, orders and users is done using the database.

## Key features

:white_check_mark: OTP authentication system: Users can authenticate using a one-time verification code (OTP).

:white_check_mark: Shopping cart: Users can add products to the shopping cart and benefit from features such as saving the shopping cart in the session.

:white_check_mark: Zarin Pal sandbox environment: using Zarin Pal API in the sandbox environment to test the payment process.

:white_check_mark: Management of addresses: the ability to create and manage multiple addresses for users, including adding, editing and deleting addresses.

:white_check_mark: Favorites list: Users can add their favorite products to the favorite list and manage it.

:white_check_mark: Order Management: Users can view the status of their orders and check the details of each order.

:white_check_mark: Search and sort products: the ability to search and sort products based on different criteria.

## :wrench: Installation and Setup (using Docker Compose)

This project uses Docker Compose to provide an isolated and easy-to-set-up development environment.

### Prerequisites

* **Docker Engine** and **Docker Compose** installed on your system.
    * [Installation guide for Docker Engine](https://docs.docker.com/engine/install/)
    * [Installation guide for Docker Compose](https://docs.docker.com/compose/install/)

### Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Loghman-Moradi/django-online-shop.git
    ```

2.  **Start the Docker containers (Django web service and PostgreSQL database):**
    This command will build the Docker images (if not already built) and start the containers in the background.
    ```bash
    docker compose up -d --build
    ```

3.  **Apply database migrations:**
    Once the containers are running, you need to apply Django's database migrations to create the necessary tables.
    ```bash
    docker compose exec web python manage.py migrate
    ```

4.  **Create a superuser (optional, for accessing Django Admin):**
    You can create an admin user to access the Django admin panel.
    ```bash
    docker compose exec web python manage.py createsuperuser
    ```

5.  **Access the application:**
    The Django development server should now be running inside the `web` container, accessible via your browser.
    Open your web browser and go to:
    [http://localhost:8000](http://localhost:8000)
