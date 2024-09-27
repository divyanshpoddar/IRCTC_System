# IRCTC Railway Management System

This project is a **Railway Management System** built with Django and MySQL. It allows users to register, login, check train seat availability, and book seats. Admins can add new trains with API key protection. The system uses token-based authentication and handles concurrent seat booking.

## Features

- User registration and login with token authentication.
- Add new trains (admin-protected via API key).
- Check seat availability between two stations.
- Book available seats on trains (race condition handling).
- View specific booking details.
- API key protection for admin endpoints.

## Tech Stack

- **Backend**: Django
- **Database**: MySQL
- **Authentication**: Token-based authentication (Django REST Framework)

## Setup Instructions

### 1. Clone the repository

bash
git clone https://github.com/your-username/irctc_system.git
cd irctc_system
2. Create a virtual environment and activate it
bash
Copy code
# On Windows
python -m venv .venv
.venv\Scripts\activate

# On macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
3. Install dependencies
bash
Copy code
pip install -r requirements.txt
4. Configure MySQL Database
Create a MySQL database:

sql
Copy code
CREATE DATABASE irctc_db;
Update the DATABASES setting in settings.py with your MySQL credentials.

5. Run Migrations
bash
Copy code
python manage.py makemigrations
python manage.py migrate
6. Create a Superuser
bash
Copy code
python manage.py createsuperuser
7. Start the development server
bash
Copy code
python manage.py runserver
The app will be available at http://127.0.0.1:8000.

API Endpoints
1. Register a User
URL: /register/
Method: POST
Payload:
json
Copy code
{
  "username": "your_username",
  "password": "your_password"
}
2. Login User
URL: /login/
Method: POST
Payload:
json
Copy code
{
  "username": "your_username",
  "password": "your_password"
}
Response: Returns an authentication token.
json
Copy code
{
  "token": "your_auth_token"
}
3. Add a New Train (Admin Only)
URL: /add_train/
Method: POST
Headers: API-Key: your_admin_api_key
Payload:
json
Copy code
{
  "train_number": "12345",
  "source": "Station A",
  "destination": "Station B",
  "total_seats": 100
}
4. Check Seat Availability
URL: /check_availability/<source>/<destination>/
Method: GET
Response:
json
Copy code
[
  {
    "train_number": "12345",
    "available_seats": 50
  }
]
5. Book a Seat (Token Required)
URL: /book_seat/<train_number>/
Method: POST
Headers: Authorization: Token your_auth_token
Response:
json
Copy code
{
  "message": "Seat booked successfully"
}
6. Get Booking Details (Token Required)
URL: /booking_details/
Method: GET
Headers: Authorization: Token your_auth_token
Response:
json
Copy code
[
  {
    "train_number": "12345",
    "seat_number": 1
  }
]
Environment Variables
Set the following environment variables for security purposes:

ADMIN_API_KEY: API key used to secure admin endpoints.
SECRET_KEY: Django secret key.
