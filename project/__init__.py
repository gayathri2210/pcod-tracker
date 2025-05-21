# project/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from flask_migrate import Migrate # REMOVED Flask-Migrate for now
import os
# from datetime import datetime # REMOVED if only used for footer year via context processor

db = SQLAlchemy()
login_manager = LoginManager()
# migrate = Migrate() # REMOVED

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a_very_secure_default_secret_key_for_simplicity')
    
    # Simplified Database Configuration (SQLite in instance folder)
    # basedir points to 'project25' if __init__.py is in 'project25/project/'
    basedir_project_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) 
    instance_folder_path = os.path.join(basedir_project_root, 'instance')
    if not os.path.exists(instance_folder_path):
        try:
            os.makedirs(instance_folder_path)
            print(f"Created instance folder: {instance_folder_path}")
        except Exception as e:
            print(f"Error creating instance folder {instance_folder_path}: {e}")
            
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(instance_folder_path, 'app_simple.db') # Using a new DB name
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # REMOVED Upload folder configurations

    db.init_app(app)
    login_manager.init_app(app)
    # migrate.init_app(app, db) # REMOVED

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # REMOVED context processor for current_year for simplicity now
    # You can add it back later if needed. For now, footer can be static.

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    # --- Create Database Tables ---
    # This will create tables based on your models if they don't exist.
    # Suitable for simple setups or when starting fresh.
    with app.app_context():
        db.create_all()
        print("Database tables checked/created via db.create_all().")

    return app
