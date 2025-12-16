from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config
from extensions import db
from auth_routes import auth_bp
from orders import orders_bp
from models import User
from dotenv import load_dotenv
import os

load_dotenv()

print("🚀 [APP START] Munchify Backend Starting...")
print(f"📁 Current directory: {os.getcwd()}")
print(f"📦 Files: {os.listdir('.')}")

def create_app():
    app = Flask(__name__)
    
    # Load configuration FIRST — Config.py already handles DB URL fixes perfectly
    app.config.from_object(Config)
    
    # Final verification of the database URI
    final_db_url = app.config.get('SQLALCHEMY_DATABASE_URI')
    if final_db_url:
        print(f"✅ [FINAL] SQLALCHEMY_DATABASE_URI: {final_db_url[:80]}...")
        print(f"   → sslmode=require: {'sslmode=require' in str(final_db_url)}")
        print(f"   → psycopg2 driver: {'psycopg2' in str(final_db_url)}")
    else:
        print("❌ [ERROR] SQLALCHEMY_DATABASE_URI is not set!")

    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)
    
    # CORS — allow all origins (temporary for testing, restrict later)
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
    
    # Only create tables in debug/local mode (never auto-create in production)
    with app.app_context():
        if app.config.get('DEBUG', False):
            print("🔧 [DEBUG MODE] Checking/Creating tables...")
            try:
                db.session.execute("SELECT 1 FROM users LIMIT 1")
                print("✅ Users table exists")
            except Exception as e:
                print(f"⚠️ Tables missing: {str(e)[:100]}...")
                print("🔄 Creating all tables...")
                try:
                    db.create_all()
                    print("✅ All tables created")
                    
                    # Create test admin if no users
                    if User.query.count() == 0:
                        admin = User(
                            username="admin",
                            email="admin@example.com",
                            is_admin=True
                        )
                        admin.password = "admin123"  # Hashed via property
                        db.session.add(admin)
                        db.session.commit()
                        print("👑 Test admin created: admin@example.com / admin123")
                except Exception as create_error:
                    print(f"❌ Failed to create tables: {create_error}")
        else:
            print("⚡ [PRODUCTION] Skipping table creation — use Flask-Migrate")

    # Health & Debug Endpoints
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
                "driver": "psycopg2" if "psycopg2" in str(final_db_url) else "unknown"
            }, 200
        except Exception as e:
            return {
                "db_status": "error",
                "error": str(e),
                "db_url_preview": str(final_db_url)[:100] if final_db_url else "None"
            }, 500
    
    @app.route('/db-status')
    def db_status():
        try:
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