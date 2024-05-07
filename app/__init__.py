from flask import Flask, current_app
import os
from config import Config
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
# JITEN SESSION
from app.main.beeWords import loadDictionary, setUpGame
# from app.main.beeWords import loadDictionary


def create_app(config_class=Config):
    
    app = Flask(__name__)
    
    app.config.from_object(config_class)
    
    app.myDictionary = loadDictionary(config=app.config, listtype="static")
    # JITEN SESSION
    # app.myGame = setUpGame(app.myDictionary.dictionaryWords) 
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

 
    if not app.debug and not app.testing:

        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/FlaskBee.log', maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('FlaskBee startup')

    return app

