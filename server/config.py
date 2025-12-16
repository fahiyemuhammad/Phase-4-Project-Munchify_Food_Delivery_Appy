import os

class Config:
    # ULTIMATE FIX FOR RENDER POSTGRESQL SSL
    # Get DATABASE_URL from environment
    raw_db_url = os.getenv("DATABASE_URL")
    
    if raw_db_url:
        # DEBUG: Show what we received
        print("=" * 50)
        print(f"🚨 [CONFIG] DATABASE_URL found from environment")
        print(f"📦 Raw URL (first 80 chars): {raw_db_url[:80]}...")
        
        # FORCE SSL MODE - THIS IS THE FIX
        # Remove any existing query parameters
        if "?" in raw_db_url:
            base = raw_db_url.split("?")[0]
            print(f"🔧 Stripped existing query params")
        else:
            base = raw_db_url
        
        # Force psycopg2 driver
        if base.startswith("postgresql://"):
            base = base.replace("postgresql://", "postgresql+psycopg2://", 1)
            print(f"🔧 Changed to psycopg2 driver")
        
        # ALWAYS add sslmode=require (Render PostgreSQL REQUIRES this)
        SQLALCHEMY_DATABASE_URI = f"{base}?sslmode=require"
        
        print(f"✅ [CONFIG] Final database URL: {SQLALCHEMY_DATABASE_URI[:80]}...")
        print("=" * 50)
    else:
        # Local development fallback
        SQLALCHEMY_DATABASE_URI = "postgresql://fahiye:strongpassword123@localhost:5432/food_order_db"
        print("⚠️  [CONFIG] Using local database - DATABASE_URL not found in environment")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-super-secret-jwt-key-change-this-in-production")
    CORS_SUPPORTS_CREDENTIALS = True
    DEBUG = True  # Set to False in production
    
    # Mail configuration (optional)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")