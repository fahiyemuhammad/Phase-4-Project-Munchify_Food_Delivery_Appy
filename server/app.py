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

    #  Allow CORS from both local and deployed frontends
    CORS(app, supports_credentials=True, origins=[
        "http://localhost:5173",
        "https://munchify-frontend.onrender.com", 
            "https://phase-4-project-munchify-food-deliv-two.vercel.app"

    ])

    api = Api(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(orders_bp)

    return app

app = create_app()