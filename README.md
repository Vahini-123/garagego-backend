# GarageGo — Django + DRF backend

Three apps:
- **accounts** — custom User (login via email, role = ADMIN/CUSTOMER), Car model, register/login/profile, admin customer management
- **services** — admin-managed service catalog (CRUD), customer-facing "active services" list
- **bookings** — ServiceRequest with a future-date booking guard and a status lifecycle
  (`PENDING → CONFIRMED → IN_PROGRESS → COMPLETED`, with `CANCELLED` available from any non-terminal state)

Auth is JWT (djangorestframework-simplejwt).

## ⚠️ About this build

This project was written in a sandbox with **no network access**, so I could not
`pip install` Django or actually run `manage.py check` / `migrate` / a live server
to confirm it end-to-end. Every file was syntax-checked (`py_compile`), and I've
built this exact app structure many times before, but **please run the steps
below yourself before trusting it with real data** — treat it as a strong first
draft, not a verified deliverable.

## Setup

```bash
cd csms-django
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Edit .env: set a real SECRET_KEY. For SQLite (default, easiest to start with),
# leave DB_ENGINE=sqlite. For MySQL, set DB_ENGINE=mysql and fill in DB_PASSWORD
# with your real password there — never hardcode it into settings.py.
```

## Run

```bash
python manage.py makemigrations accounts services bookings
python manage.py migrate
python manage.py seed_data          # creates admin@csms.local / ChangeMe123! + 5 starter services
python manage.py runserver
```

Then hit `POST /api/accounts/login/` with that admin email/password to get a JWT,
change the seeded password immediately, and go from there.

## Switching to MySQL

1. Make sure MySQL is running and a database exists (`CREATE DATABASE csms_db;`).
2. In `.env`: `DB_ENGINE=mysql`, plus `DB_NAME` / `DB_USER` / `DB_PASSWORD` / `DB_HOST` / `DB_PORT`.
3. Re-run `migrate` against it.

The project uses PyMySQL (pure Python, no system MySQL dev headers needed) shimmed
in as the `MySQLdb` driver via `config/__init__.py`.

## Key endpoints

| Method | Path | Who | Purpose |
|---|---|---|---|
| POST | `/api/accounts/register/` | public | customer signup |
| POST | `/api/accounts/login/` | public | returns JWT access/refresh + user |
| POST | `/api/auth/refresh/` | authenticated | refresh access token |
| GET/PATCH | `/api/accounts/me/` | authenticated | own profile |
| CRUD | `/api/accounts/cars/` | authenticated | own cars |
| GET | `/api/accounts/admin/customers/` | admin | list customers |
| CRUD | `/api/services/` | admin write / any read | service catalog |
| GET | `/api/services/active/` | authenticated | active services only |
| POST | `/api/bookings/` | authenticated | create booking (future-date guard applies) |
| GET | `/api/bookings/mine/` | authenticated | own bookings |
| GET | `/api/bookings/admin/all/` | admin | all bookings, filterable by `?status=`, `?scheduled_date=`, `?service_type=` |
| PATCH | `/api/bookings/<id>/status/` | admin | move status forward (enforces the allowed-transition map) |

## Business rules implemented

- **Dynamic service catalog**: admins CRUD `ServiceType`; customers only ever see `is_active=True` entries.
- **Future-date booking guard**: `ServiceRequestCreateSerializer.validate()` rejects any `scheduled_date`+`scheduled_time` that isn't strictly in the future, using timezone-aware comparison.
- **Status sync**: `ServiceRequest.ALLOWED_TRANSITIONS` is the single source of truth for what status changes are legal; both the admin update endpoint and the model itself enforce it, so the customer and admin panels can't drift out of sync.
