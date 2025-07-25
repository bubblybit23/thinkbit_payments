import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

def create_app():
    app = Flask(__name__)
    
    # Secure configuration from .env
    app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET", "default_secret")
    app.config['DB_CONFIG'] = {
        'host': os.getenv("DB_HOST", "localhost"),
        'port': os.getenv("DB_PORT", 5432),
        'user': os.getenv("DB_USER", "postgres"),
        'password': os.getenv("DB_PASSWORD", ""),
        'dbname': os.getenv("DB_NAME", "thinkbit_payments")
    }
    
    from . import routes
    app.register_blueprint(routes.bp)
    
    return app