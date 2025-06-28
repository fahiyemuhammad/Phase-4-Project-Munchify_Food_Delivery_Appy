from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config
from server.extensions import db
from server.auth_routes import auth_bp
from server.orders import orders_bp  # ✅ Added import
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)
    CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

    api = Api(app)

    # ✅ Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(orders_bp)  # ✅ Orders routes registered here

    return app