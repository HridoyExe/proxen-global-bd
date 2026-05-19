# Proxen Global E-commerce Backend

Welcome to the **Proxen Global E-commerce Backend** repository. This project is a robust, production-ready REST API built with Django and Django REST Framework to power the Proxen Global E-commerce platform. It provides a secure and scalable foundation for managing products, users, and orders, designed to seamlessly integrate with modern front-end applications.

## 🚀 Key Features

- **Custom User Authentication**: Secure JWT-based authentication using `djangorestframework-simplejwt`.
- **Advanced Product Management**: Comprehensive APIs for managing products, including SKU tracking, stock management, categories, and dynamic discount pricing.
- **Robust API Documentation**: Interactive, auto-generated API documentation using Swagger (via `drf-yasg`) and ReDoc.
- **Filtering & Pagination**: Efficient data retrieval with global pagination and advanced filtering/sorting capabilities using `django-filter`.
- **Data Validation**: Strict input validation to ensure data integrity and prevent invalid operations.

## 🛠️ Technology Stack

- **Language**: Python 3
- **Framework**: Django & Django REST Framework (DRF)
- **Authentication**: JWT (JSON Web Tokens)
- **Database**: SQLite (Development) / PostgreSQL (Ready for Production)
- **Documentation**: Swagger UI & ReDoc (`drf-yasg`)
- **Image Processing**: Pillow

## 📂 Project Structure

```text
proxen-global-bd/
├── proxen_global_bd/      # Core Django settings and configuration
├── product/               # Product management app (models, views, serializers)
├── user/                  # Custom user and authentication app
├── requirements.txt       # Project dependencies
├── manage.py              # Django command-line utility
└── .env                   # Environment variables (not tracked in git)
```

## ⚙️ Local Setup and Installation

Follow these steps to set up the project locally on your machine.

### Prerequisites
- Python 3.9+
- pip (Python package installer)
- virtualenv (Recommended)

### 1. Clone the repository

```bash
git clone <repository-url>
cd "Proxen Global Bd"
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv .proxen_env
.\.proxen_env\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv .proxen_env
source .proxen_env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

Make sure to configure your `.env` file in the root directory for your environment settings (e.g., SECRET_KEY, DEBUG mode).

### 5. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Load Dummy Data (Optional)

If you need initial testing data, load the provided fixtures:
```bash
python manage.py loaddata product/fixtures/dummy_data.json
```

### 7. Create a Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 8. Run the Development Server

```bash
python manage.py runserver
```

The API will now be accessible at `http://127.0.0.1:8000/`.

## 📚 API Documentation

Once the server is running, you can explore the available API endpoints using the interactive documentation:

- **Swagger UI**: `http://127.0.0.1:8000/swagger/` (or your configured swagger path)
- **ReDoc**: `http://127.0.0.1:8000/redoc/`

## 🔒 Authentication Flow

1. **Login**: Authenticate with valid credentials to receive `access` and `refresh` tokens.
2. **Access**: Include the access token in the header of protected requests: `Authorization: Bearer <your_access_token>`.
3. **Refresh**: Use your refresh token to get a new access token when it expires.

---
*Built for Proxen Global E-commerce Platform.*
