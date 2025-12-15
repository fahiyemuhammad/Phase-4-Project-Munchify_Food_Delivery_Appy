from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config
from extensions import db
from auth_routes import auth_bp
from orders import orders_bp
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # MANUAL CONFIGURATION AS BACKUP (Add this)
    # This ensures the SSL parameter is always added
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        print(f"🚨 MANUAL CHECK: DATABASE_URL exists: {database_url[:50]}...")
        
        # Double-check SSL mode
        if "sslmode=" not in database_url.lower():
            print("🚨 WARNING: DATABASE_URL missing sslmode, fixing...")
            if "?" not in database_url:
                database_url += "?sslmode=require"
            else:
                database_url += "&sslmode=require"
        
        # Ensure psycopg2 driver
        if database_url.startswith("postgresql://"):
            database_url = database_url.replace("postgresql://", "postgresql+psycopg2://", 1)
        
        # Manually set it
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        print(f"✅ MANUAL FIX applied: {app.config['SQLALCHEMY_DATABASE_URI'][:60]}...")
    
    # Now load from Config class
    app.config.from_object(Config)
    
    # Verify final config
    print(f"🔍 FINAL SQLALCHEMY_DATABASE_URI: {app.config.get('SQLALCHEMY_DATABASE_URI', 'NOT SET')}")

    db.init_app(app)
    Migrate(app, db)

    # UPDATED CORS configuration
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "allow_headers": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
            "supports_credentials": True
        }
    })

    api = Api(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(orders_bp)

    return app

app = create_app()

# Add this at the end to verify app starts
if __name__ != "__main__":
    print("🎉 Flask app initialized successfully!")
    print(f"📊 Database configured: {'postgresql' in str(app.config.get('SQLALCHEMY_DATABASE_URI', '')).lower()}")