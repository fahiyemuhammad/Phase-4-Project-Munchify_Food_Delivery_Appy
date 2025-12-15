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