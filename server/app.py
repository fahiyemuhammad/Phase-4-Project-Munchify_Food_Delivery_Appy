from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config
from extensions import db, bcrypt, jwt, mail
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

    final_db_url = app.config.get("SQLALCHEMY_DATABASE_URI")
    print(f"✅ [FINAL] SQLALCHEMY_DATABASE_URI: {final_db_url[:80]}...")

    # Init extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    Migrate(app, db)

    # 🔥 CRITICAL: always cleanup session
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

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

    app.register_blueprint(auth_bp)
    app.register_blueprint(orders_bp)

    with app.app_context():
        if app.config.get("DEBUG", False):
            try:
                db.session.execute("SELECT 1 FROM users LIMIT 1")
            except Exception:
                db.create_all()

    @app.route("/")
    def home():
        return {"message": "Munchify Backend API", "status": "running"}, 200

    @app.route("/health")
    def health():
        return {"status": "healthy"}, 200

    @app.route("/test-db")
    def test_db():
        try:
            db.session.execute("SELECT 1")
            return {"db": "connected"}, 200
        except Exception as e:
            return {"db": "error", "error": str(e)}, 500

    print("🎉 [APP READY] Flask app initialized")
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
else:
    print("⚡ [PRODUCTION] Running on Render")
