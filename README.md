# Netfix Project

Netfix is a Django service-based application allowing companies to list services and customers to request services. The app provides profiles for both customers and companies, enabling service management, requests, and user authentication.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
- [Testing](#testing)
- [License](#license)

---

## Features

- **User Authentication**: Company and customer login and registration.
- **Profile Management**: Separate profiles for customers and companies.
- **Service Management**: Companies can create, edit, and delete services.
- **Service Requests**: Customers can request services from available providers.
- **Pagination**: Service listings are paginated for improved UI.
- **Admin Panel**: Django's built-in admin panel for database management.

---
## Project Structure

```plaintext
netfix/
├── main/                   # Core app with basic site views
├── users/                  # Users app, handling authentication and profile management
├── services/               # Services app, handling service creation and requests
├── netfix/                 # Project settings and configurations
│   ├── settings.py         # Main configuration file
│   ├── urls.py             # URL routing for the project
│   └── wsgi.py             # WSGI entry point
├── static/                 # Static files (CSS, JS, Images)
├── templates/              # HTML templates for the project
├── manage.py               # Django management script
└── README.md               # Project README file
```
## Technologies Used
- **Django**: High-level Python web framework for rapid development.
- **SQLite**: Lightweight database for development (configurable to other databases for production).
- **CSS**: styling frontend.
- **HTML**

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/netfix.git
   cd netfix
   ```
2. **Set up a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3. **Install required packages:**:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration
1. **Database Setup**: Ensure that your database configuration is correctly set up in ```netfix/settings.py```.

2. **Static Files**: Collect static files using:

    ```bash
    python manage.py collectstatic
    ```
3. **Migrations**: Run migrations to set up the database schema:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
4. **Superuser**: Create a superuser for admin access:
    ```bash
    python manage.py createsuperuser
    ```
## Running the Project
1. **Start the development server**:
    ```bash
    python manage.py runserver
    ```
2. **Access the application**: Open your browser and visit http://127.0.0.1:8000.


3. **Admin Panel**: Visit http://127.0.0.1:8000/admin to access the Django admin panel.

## Testing
- To run tests, execute:
    ```bash
    python manage.py test
    ```
## License
This project is licensed under the MIT License. See the LICENSE file for details.

