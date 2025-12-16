import os

class Config:
    # Ultimate fix for Render PostgreSQL
    raw_db_url = os.getenv("DATABASE_URL")
    
    if raw_db_url:
        print("=" * 50)
        print(f"🚨 [CONFIG] DATABASE_URL found")
        print(f"📦 Raw URL (first 80 chars): {raw_db_url[:80]}...")
        
        # Strip existing query params if any
        if "?" in raw_db_url:
            base = raw_db_url.split("?")[0]
        else:
            base = raw_db_url
        
        # Force psycopg2 driver
        if base.startswith("postgresql://"):
            base = base.replace("postgresql://", "postgresql+psycopg2://", 1)
        
        # Always require SSL
        SQLALCHEMY_DATABASE_URI = f"{base}?sslmode=require"
        
        print(f"✅ [CONFIG] Final DB URL: {SQLALCHEMY_DATABASE_URI[:80]}...")
        print("=" * 50)
    else:
        # Local fallback
        SQLALCHEMY_DATABASE_URI = "postgresql://fahiye:strongpassword123@localhost:5432/food_order_db"
        print("⚠️ [CONFIG] Using local DB — no DATABASE_URL in env")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-super-secret-jwt-key-change-in-prod")
    CORS_SUPPORTS_CREDENTIALS = True
    
    # Better: Use env var in production
    DEBUG = os.getenv("FLASK_DEBUG", "False") == "True"
    
    # Mail (optional)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")