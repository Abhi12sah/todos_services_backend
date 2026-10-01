# todos_services_backend
A secure Todo REST API built with FastAPI, PostgreSQL, SQLAlchemy, Alembic, JWT authentication, and Pytest.

#Features:
User CRUD,
Todo CRUD,
PostgreSQL database,
SQLAlchemy ORM,
Alembic migrations,
Password hashing,
JWT login,
Validation and error handling,
Swagger documentation,
CORS support,
Pytest tests,

#Project Structure:

app/
├── core/          # Security and JWT
├── db/            # Database connection
├── exceptions/    # Custom exceptions
├── models/        # Database models
├── routers/       # API routes
├── schemas/       # Request/response schemas
├── services/      # Business logic
├── tests/         # Tests
├── config.py      # Environment settings
└── main.py        # FastAPI application

alembic/           # Database migrations
.env               # Local configuration
requirements.txt   # Python packages


#Requirements:
Python 3.12+
PostgreSQL
VS Code
Virtual environment


1. Create and activate virtual environment:
#Windows PowerShell:
python -m venv venv
#window: .\venv\Scripts\Activate.ps1    #mac: source venv/bin/activate

2. Install packages:
pip install -r requirements.txt

















