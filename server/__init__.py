from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config
from extensions import db, bcrypt, jwt, mail
from auth_routes import auth_bp
from orders import orders_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    #  Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    Migrate(app, db)

    #  CORS: Allow frontend at localhost:5173 with all needed methods
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "allow_headers": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
            "supports_credentials": True
        }
    })

    #  Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(orders_bp)

    return app
