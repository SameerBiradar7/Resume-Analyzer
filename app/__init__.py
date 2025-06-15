from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
import os

def create_app(config_class=Config):
    app = Flask(__name__,
                static_folder=os.path.join('main', 'static'),
                template_folder=os.path.join('main', 'templates'))
    
    app.config.from_object(config_class)
    Bootstrap(app)
    
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app
