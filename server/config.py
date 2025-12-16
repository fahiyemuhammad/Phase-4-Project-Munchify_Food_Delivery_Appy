import os

class Config:
    raw_db_url = os.getenv("DATABASE_URL")

    if raw_db_url:
        print("=" * 50)
        print("🚨 [CONFIG] DATABASE_URL found")
        print(f"📦 Raw URL (first 80 chars): {raw_db_url[:80]}...")

        # Strip existing query params
        base = raw_db_url.split("?")[0]

        # Force psycopg2 driver
        if base.startswith("postgresql://"):
            base = base.replace(
                "postgresql://",
                "postgresql+psycopg2://",
                1
            )

        # Enforce SSL via URL
        SQLALCHEMY_DATABASE_URI = f"{base}?sslmode=require"

        print(f"✅ [CONFIG] Final DB URL: {SQLALCHEMY_DATABASE_URI[:80]}...")
        print("=" * 50)
    else:
        SQLALCHEMY_DATABASE_URI = (
            "postgresql+psycopg2://fahiye:strongpassword123@localhost:5432/food_order_db"
        )
        print("⚠️ [CONFIG] Using local DB")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 🔥 RENDER-SAFE ENGINE CONFIG (IMPORTANT)
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "pool_size": 5,
        "max_overflow": 10,
    }

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "your-super-secret-jwt-key-change-in-prod"
    )

    CORS_SUPPORTS_CREDENTIALS = True
    DEBUG = os.getenv("FLASK_DEBUG", "False") == "True"

    # Mail (optional)
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
