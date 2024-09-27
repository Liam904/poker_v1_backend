from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
import os
from .models import db
from dotenv import load_dotenv

load_dotenv()

bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///game.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # JWT configuration
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "default_secret")
    app.config["JWT_TOKEN_LOCATION"] = [
        "headers",
        "cookies",
    ]  # Adjust based on your needs
    app.config["JWT_COOKIE_SECURE"] = False  # Set to True in production with HTTPS
    app.config["JWT_ACCESS_COOKIE_PATH"] = "/"  # Path for the access token cookie

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)  # Initialize JWTManager with the app
    migrate.init_app(app, db)
    CORS(app)

    # Register blueprints
    from .views import views
    from .auth_routes import auth

    app.register_blueprint(views)
    app.register_blueprint(auth)

    return app
