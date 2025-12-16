from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config
from extensions import db
from auth_routes import auth_bp
from orders import orders_bp
from models import User, MenuItem, Order, OrderItem
from dotenv import load_dotenv
import os

load_dotenv()

print("🚀 [APP START] Munchify Backend Starting...")
print(f"📁 Current directory: {os.getcwd()}")
print(f"📦 Files: {os.listdir('.')}")

def create_app():
    app = Flask(__name__)
    
    # EMERGENCY OVERRIDE: Direct database URL setting
    db_url_from_env = os.getenv("DATABASE_URL")
    
    if db_url_from_env:
        print(f"📦 [ENV] DATABASE_URL found: {db_url_from_env[:60]}...")
        
        # FORCE SSL
        if "sslmode=" not in db_url_from_env.lower():
            if "?" in db_url_from_env:
                fixed_url = db_url_from_env + "&sslmode=require"
            else:
                fixed_url = db_url_from_env + "?sslmode=require"
        else:
            fixed_url = db_url_from_env
            
        # Force psycopg2 driver
        if fixed_url.startswith("postgresql://"):
            fixed_url = fixed_url.replace("postgresql://", "postgresql+psycopg2://", 1)
            
        print(f"🔧 [FIX] Setting DB URL: {fixed_url[:70]}...")
        app.config['SQLALCHEMY_DATABASE_URI'] = fixed_url
    else:
        print("⚠️  [INFO] DATABASE_URL not found in environment (normal for local)")
        # Use config.py which has fallback
        app.config.from_object(Config)
    
    # Load the rest of config
    app.config.from_object(Config)
    
    # Verify what we have
    final_db_url = app.config.get('SQLALCHEMY_DATABASE_URI', 'NOT SET')
    print(f"✅ [VERIFY] Final DB URL: {final_db_url[:80]}...")
    print(f"✅ [VERIFY] Has SSL: {'sslmode=require' in str(final_db_url)}")
    print(f"✅ [VERIFY] Using psycopg2: {'psycopg2' in str(final_db_url)}")
    
    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)
    
    # CORS - allow everything
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "allow_headers": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
            "supports_credentials": True
        }
    })
    
    api = Api(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(orders_bp)
    
    # CRITICAL: Create tables if they don't exist (ONLY IN DEVELOPMENT)
    # In production, we should use migrations, but this ensures tables exist
    with app.app_context():
        if app.config.get('DEBUG', False):
            print("🔧 [DEBUG MODE] Checking/Creating tables...")
            try:
                # Try to query users table to see if it exists
                db.session.execute("SELECT 1 FROM users LIMIT 1")
                print("✅ Users table exists")
            except Exception as e:
                print(f"⚠️  Tables don't exist: {str(e)[:100]}...")
                print("🔄 Creating all tables...")
                try:
                    db.create_all()
                    print("✅ All tables created successfully")
                    
                    # Create a test admin user if no users exist
                    if User.query.count() == 0:
                        admin = User(
                            username="admin",
                            email="admin@example.com",
                            is_admin=True
                        )
                        admin.password = "admin123"  # Triggers hashing
                        db.session.add(admin)
                        db.session.commit()
                        print("👑 Test admin user created: admin@example.com / admin123")
                        
                except Exception as create_error:
                    print(f"❌ Failed to create tables: {create_error}")
        else:
            print("⚡ [PRODUCTION] Skipping auto table creation - use migrations")
    
    # Add health check endpoints
    @app.route('/')
    def home():
        return {"message": "Munchify Backend API", "status": "running"}, 200
    
    @app.route('/health')
    def health():
        return {"status": "healthy", "service": "munchify-backend"}, 200
    
    @app.route('/test-db')
    def test_db():
        try:
            db.session.execute("SELECT 1")
            return {
                "db_status": "connected",
                "has_ssl": "sslmode=require" in str(final_db_url),
                "tables_exist": True
            }, 200
        except Exception as e:
            return {
                "db_status": "error",
                "error": str(e),
                "db_url_preview": str(final_db_url)[:100]
            }, 500
    
    @app.route('/db-status')
    def db_status():
        try:
            # Check if tables exist
            tables = ['users', 'menu_items', 'orders', 'order_items']
            status = {}
            for table in tables:
                try:
                    db.session.execute(f"SELECT 1 FROM {table} LIMIT 1")
                    status[table] = "exists"
                except:
                    status[table] = "missing"
            
            return {
                "status": "connected",
                "tables": status,
                "user_count": User.query.count()
            }, 200
        except Exception as e:
            return {"status": "error", "error": str(e)}, 500
    
    print("🎉 [APP READY] Flask app initialized successfully")
    return app

app = create_app()

if __name__ == "__main__":
    print("🌍 [SERVER] Starting development server on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
else:
    print("⚡ [PRODUCTION] Running in production mode on Render")