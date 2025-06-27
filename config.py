import os

class Config:
    # PostgreSQL connection
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", 
        "postgresql://fahiye:strongpassword123@localhost:5432/food_order_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT secret
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")

    # Allow credentials for cross-origin
    CORS_SUPPORTS_CREDENTIALS = True

    # Optional: Enable debug in dev
    DEBUG = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")