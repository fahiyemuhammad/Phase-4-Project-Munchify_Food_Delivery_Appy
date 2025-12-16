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

    # Load config FIRST
    app.config.from_object(Config)

    # Verify DB config
    final_db_url = app.config.get("SQLALCHEMY_DATABASE_URI")
    if final_db_url:
        print(f"✅ [FINAL] SQLALCHEMY_DATABASE_URI: {final_db_url[:80]}...")
        print(f"   → sslmode=require: {'sslmode=require' in final_db_url}")
        print(f"   → psycopg2 driver: {'psycopg2' in final_db_url}")
    else:
        print("❌ [ERROR] SQLALCHEMY_DATABASE_URI not set")

    # Init extensions
    db.init_app(app)
    Migrate(app, db)

    # 🔥 REQUIRED FOR NULLPOOL (CRITICAL FIX)
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    # CORS (open for now)
    CORS(
        app,
        resources={
            r"/*": {
                "origins": "*",
                "allow_headers": "*",
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
                "supports_credentials": True,
            }
        },
    )

    api = Api(app)

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(orders_bp)

    # Local-only table checks
    with app.app_context():
        if app.config.get("DEBUG", False):
            print("🔧 [DEBUG MODE] Checking tables...")
            try:
                db.session.execute("SELECT 1 FROM users LIMIT 1")
                print("✅ Users table exists")
            except Exception as e:
                print(f"⚠️ Tables missing: {str(e)[:100]}...")
                print("🔄 Creating tables...")
                try:
                    db.create_all()
                    print("✅ Tables created")

                    if User.query.count() == 0:
                        admin = User(
                            username="admin",
                            email="admin@example.com",
                            is_admin=True,
                        )
                        admin.password = "admin123"
                        db.session.add(admin)
                        db.session.commit()
                        print("👑 Admin created")
                except Exception as err:
                    print(f"❌ Failed to create tables: {err}")
        else:
            print("⚡ [PRODUCTION] Skipping table creation")

    # Routes
    @app.route("/")
    def home():
        return {"message": "Munchify Backend API", "status": "running"}, 200

    @app.route("/health")
    def health():
        return {"status": "healthy", "service": "munchify-backend"}, 200

    @app.route("/test-db")
    def test_db():
        try:
            db.session.execute("SELECT 1")
            return {
                "db_status": "connected",
                "ssl": "enabled",
                "driver": "psycopg2",
            }, 200
        except Exception as e:
            return {
                "db_status": "error",
                "error": str(e),
            }, 500

    print("🎉 [APP READY] Flask app initialized")
    return app

app = create_app()

if __name__ == "__main__":
    print("🌍 [DEV] Running on http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
else:
    print("⚡ [PRODUCTION] Running on Render")
