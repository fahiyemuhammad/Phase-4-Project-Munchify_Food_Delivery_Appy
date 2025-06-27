from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config
from server.extensions import db, bcrypt, jwt, mail
from server.auth_routes import auth_bp
from server.orders import orders_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ✅ Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    Migrate(app, db)

    # ✅ CORS: Allow frontend at localhost:5173 with all needed methods
    CORS(
        app,
        origins=["http://localhost:5173"],
        supports_credentials=True,
        methods=["GET", "POST", "PATCH", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"]
    )

    # ✅ Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(orders_bp)

    return app
