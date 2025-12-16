import os
import sqlalchemy  # Needed for NullPool if you enable it

class Config:
    raw_db_url = os.getenv("DATABASE_URL")
    
    if raw_db_url:
        print("=" * 50)
        print(f"🚨 [CONFIG] DATABASE_URL found")
        print(f"📦 Raw URL (first 80 chars): {raw_db_url[:80]}...")
        
        # Strip existing query params
        if "?" in raw_db_url:
            base = raw_db_url.split("?")[0]
        else:
            base = raw_db_url
        
        # Force psycopg2 driver
        if base.startswith("postgresql://"):
            base = base.replace("postgresql://", "postgresql+psycopg2://", 1)
        
        # Require SSL
        SQLALCHEMY_DATABASE_URI = f"{base}?sslmode=require"
        
        print(f"✅ [CONFIG] Final DB URL: {SQLALCHEMY_DATABASE_URI[:80]}...")
        print("=" * 50)
    else:
        SQLALCHEMY_DATABASE_URI = "postgresql://fahiye:strongpassword123@localhost:5432/food_order_db"
        print("⚠️ [CONFIG] Using local DB")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # FIX FOR RENDER POSTGRES: Handle stale/killed connections
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,      # Test connection before use (discards dead ones)
        "pool_recycle": 300,        # Recycle connections every 5 minutes
        "pool_size": 5,             # Small pool (good for low-traffic)
        "max_overflow": 10,         # Allow temporary extra connections
        "pool_timeout": 30,         # Wait max 30s for a connection
        # OPTIONAL TEMP FIX: Disable pooling entirely (100% reliable, minor perf cost)
        # "poolclass": sqlalchemy.pool.NullPool
    }

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-super-secret-jwt-key-change-in-prod")
    CORS_SUPPORTS_CREDENTIALS = True
    DEBUG = os.getenv("FLASK_DEBUG", "False") == "True"

    # Mail config (optional)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")