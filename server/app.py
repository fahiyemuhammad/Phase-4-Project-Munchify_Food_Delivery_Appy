from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config
from extensions import db
from auth_routes import auth_bp
from orders import orders_bp
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)

    # TEMPORARY FIX: Allow all origins (use only for debugging!)
    # This will allow requests from any frontend, including your Vercel deployment
    CORS(
        app,
        origins="*",                    # Allows every origin
        supports_credentials=True,      # Keep this if you're sending cookies or auth headers later
        allow_headers="*",              # Allows all headers (Content-Type, Authorization, etc.)
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]
    )

    api = Api(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(orders_bp)

    return app

app = create_app()