# IRCTC Railway Management System

This project is a **Railway Management System** built using **Django** and **MySQL**. It allows users to register, log in, check train seat availability, and book seats. Admins can manage trains and add new ones. The system uses token-based authentication for users and API key protection for admin endpoints. The booking system also handles concurrent seat booking using database-level locking.

## Features

- User registration and login with token-based authentication.
- Admin can add new trains (protected by API key).
- Users can check seat availability for trains between two stations.
- Users can book available seats on a train (race condition handling is in place).
- Users can view their booking details.
- Admin API endpoints are protected with an API key.

---

## Tech Stack

- **Backend**: Django
- **Database**: MySQL
- **Authentication**: Django REST Framework (Token-based authentication)

---

## Prerequisites

- Python 3.x
- MySQL
- Git

---

## Project Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/irctc_system.git
cd irctc_system
```

### 2. Create a Virtual Environment and Activate it

```bash
# On Windows
python -m venv .venv
.venv\Scripts\activate

# On macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the Required Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL Database

- **Create a MySQL database**:
  ```sql
  CREATE DATABASE irctc_db;
  ```

- Update the `DATABASES` setting in `irctc_system/settings.py` with your MySQL credentials:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'irctc_db',
        'USER': 'your_mysql_user',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 5. Apply Migrations

Run the following commands to set up the database schema:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser

```bash
python manage.py createsuperuser
```

This will allow you to access the Django admin panel for managing trains.

### 7. Set Up API Key for Admin Actions

In the `settings.py` file, add a secret API key for admin operations:

```python
ADMIN_API_KEY = 'your_secret_api_key'
```

### 8. Start the Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`.

---

## API Endpoints

### **1. Register a User**

- **URL**: `/register/`
- **Method**: `POST`
- **Payload**:
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```
- **Response**:
  ```json
  {
    "message": "User created successfully"
  }
  ```

---

### **2. Login User**

- **URL**: `/login/`
- **Method**: `POST`
- **Payload**:
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```
- **Response**:
  ```json
  {
    "token": "your_auth_token"
  }
  ```

---

### **3. Add a New Train (Admin Only)**

- **URL**: `/add_train/`
- **Method**: `POST`
- **Headers**: `API-Key: your_admin_api_key`
- **Payload**:
  ```json
  {
    "train_number": "12345",
    "source": "Station A",
    "destination": "Station B",
    "total_seats": 100
  }
  ```
- **Response**:
  ```json
  {
    "message": "Train added successfully"
  }
  ```

---

### **4. Check Seat Availability**

- **URL**: `/check_availability/<source>/<destination>/`
- **Method**: `GET`
- **Response**:
  ```json
  [
    {
      "train_number": "12345",
      "available_seats": 50
    }
  ]
  ```

---

### **5. Book a Seat (Token Required)**

- **URL**: `/book_seat/<train_number>/`
- **Method**: `POST`
- **Headers**: `Authorization: Token your_auth_token`
- **Response**:
  ```json
  {
    "message": "Seat booked successfully"
  }
  ```

---

### **6. Get Booking Details (Token Required)**

- **URL**: `/booking_details/`
- **Method**: `GET`
- **Headers**: `Authorization: Token your_auth_token`
- **Response**:
  ```json
  [
    {
      "train_number": "12345",
      "seat_number": 1
    }
  ]
  ```

---

## Environment Variables

Set the following environment variables for security purposes:

- `ADMIN_API_KEY`: API key used to secure admin endpoints.
- `SECRET_KEY`: Django secret key.
