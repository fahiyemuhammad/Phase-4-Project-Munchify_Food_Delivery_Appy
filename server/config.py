import os
from urllib.parse import urlparse

class Config:
    # PostgreSQL connection - FIXED for Render PostgreSQL SSL
    database_url = os.getenv("DATABASE_URL")
    
    if database_url:
        # Parse the URL to handle it properly
        parsed_url = urlparse(database_url)
        
        # Force SSL mode for Render PostgreSQL
        if "sslmode" not in parsed_url.query:
            # Append sslmode=require if not already present
            query = f"{parsed_url.query}&sslmode=require" if parsed_url.query else "sslmode=require"
            # Reconstruct the URL with SSL requirement
            SQLALCHEMY_DATABASE_URI = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{query}"
        else:
            SQLALCHEMY_DATABASE_URI = database_url
            
        # Ensure we're using psycopg2 driver (Render's default)
        if SQLALCHEMY_DATABASE_URI.startswith("postgresql://"):
            SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
                "postgresql://", "postgresql+psycopg2://", 1
            )
    else:
        # Fallback for local development
        SQLALCHEMY_DATABASE_URI = "postgresql://fahiye:strongpassword123@localhost:5432/food_order_db"

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