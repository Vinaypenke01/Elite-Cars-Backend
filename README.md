# Car Reseller Backend - Elite Motors

Professional Django REST Framework backend for Elite Motors car dealership platform.

## Project Structure

```
car_reseller_backend/
│
├── config/                 # Project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/                   # Feature applications
│   ├── accounts/           # Authentication & user management
│   ├── cars/               # Car inventory management
│   │   ├── models/         # Car, Settings, RecentlySold
│   │   ├── serializers/    # Data serialization
│   │   ├── views/          # API endpoints
│   │   ├── admin.py
│   │   └── urls.py
│   └── orders/             # Booking/order management
│
├── core/                   # Shared utilities
│   ├── permissions.py      # Custom permissions
│   ├── pagination.py       # Pagination classes
│   ├── responses.py        # Standard responses
│   └── exceptions.py       # Exception handlers
│
├── services/               # Business logic layer
│   ├── car_service.py
│   ├── auth_service.py
│   └── settings_service.py
│
├── common/                 # Shared helpers
│   ├── constants.py        # Application constants
│   ├── utils.py            # Utility functions
│   └── validators.py       # Custom validators
│
├── media/                  # User uploads
├── static/                 # Static files
├── manage.py
└── requirements.txt
```

## Quick Start

### 1. Install Dependencies

```bash
git clone https://github.com/Vinaypenke01/Elite-Cars-Backend.git
cd Elite-Cars-Backend
pip install -r requirements.txt
```

### 2. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser

```bash
python manage.py createsuperuser
```

### 4. Run Development Server

```bash
python manage.py runserver 8000
```

## API Endpoints

### Base URL: `http://localhost:8000/api/v1/`

- **Cars**: `/api/v1/cars/`
- **Orders**: `/api/v1/orders/bookings/`
- **Auth**: `/api/v1/accounts/`

## Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Features

- ✅ Layered architecture (Models → Serializers → Services → Views)
- ✅ Custom permissions and pagination
- ✅ Standard API responses
- ✅ Comprehensive validation
- ✅ Business logic separation
- ✅ Modular app structure

## Apps

### Accounts
- Admin registration & authentication
- Token-based auth
- User profiles

### Cars
- Car inventory management
- Dealership settings
- Recently sold vehicles

### Orders
- Booking management
- Status updates
- Package selection

## Admin Panel

Access at: `http://localhost:8000/admin/`

## License

MIT License
