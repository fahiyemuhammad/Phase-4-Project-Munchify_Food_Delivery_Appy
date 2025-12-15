import os

class Config:
    # NUCLEAR OPTION: Hardcoded SSL fix for Render
    # Get DATABASE_URL from environment
    raw_url = os.getenv("DATABASE_URL")
    
    if raw_url:
        # Step 1: Print what we got
        print(f"🚀 RAW DATABASE_URL: {raw_url}")
        
        # Step 2: FORCE sslmode=require NO MATTER WHAT
        # Remove any existing query parameters
        base_url = raw_url.split('?')[0] if '?' in raw_url else raw_url
        
        # Step 3: Use psycopg2 driver
        if base_url.startswith("postgresql://"):
            base_url = base_url.replace("postgresql://", "postgresql+psycopg2://", 1)
        
        # Step 4: ALWAYS add sslmode=require
        SQLALCHEMY_DATABASE_URI = f"{base_url}?sslmode=require"
        
        print(f"🎯 FORCED DATABASE_URL: {SQLALCHEMY_DATABASE_URI}")
    else:
        # Local development
        SQLALCHEMY_DATABASE_URI = "postgresql://fahiye:strongpassword123@localhost:5432/food_order_db"
        print("🏠 Using local database")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")
    CORS_SUPPORTS_CREDENTIALS = True
    DEBUG = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")