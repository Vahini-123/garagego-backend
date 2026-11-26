# GarageGo: Backend

Django REST API for GarageGo, a car service booking app.

**Live site:** https://garagego-frontend.netlify.app
**Frontend repository:** https://github.com/Vahini-123/garagego-frontend

## Features
- JWT login for customers and admins
- Customers add cars and book services; admins manage the service catalog and all requests
- Status workflow: Pending → Confirmed → In Progress → Completed (or Cancelled)
- Estimated completion date for each request
- Email notifications on status changes
- Forgot password with an emailed reset link

## Tech stack
Python, Django, Django REST Framework, Simple JWT, SQLite. Hosted on PythonAnywhere.

## Main endpoints
| Endpoint | Purpose |
|---|---|
| `POST /api/accounts/register/` | Customer sign-up |
| `POST /api/accounts/login/` | Login, returns access and refresh tokens |
| `GET /api/accounts/me/` | Current user |
| `POST /api/accounts/password-reset/` | Send a reset link |
| `POST /api/accounts/password-reset/confirm/` | Set a new password |
| `GET/POST /api/accounts/cars/` | A customer's cars |
| `GET /api/services/active/` | Active services (customers) |
| `/api/services/` | Service catalog (admin) |
| `POST /api/bookings/` | Create a booking |
| `GET /api/bookings/mine/` | A customer's bookings |
| `GET /api/bookings/admin/all/` | All bookings (admin) |
| `PATCH /api/bookings/<id>/status/` | Update status and estimate (admin) |

## Run locally (Windows)
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Environment variables
Set these in a `.env` file. Never commit it.

| Name | Purpose |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` locally, `False` in production |
| `ALLOWED_HOSTS` | Comma-separated hostnames |
| `FRONTEND_URL` | Address of the frontend (used for CORS and reset links) |
| `EMAIL_HOST_USER` | Sender Gmail address |
| `EMAIL_HOST_PASSWORD` | Gmail app password |
