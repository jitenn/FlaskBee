from flask import Flask, current_app
import os
from flask_moment import Moment
from config import Config
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from app.main.beeWords import loadDictionary, setUpGame


moment = Moment()
# Load the dictonary
# myDictionary = loadDictionary()
# myGame = setUpGame(myDictionary.dictionaryWords)
# print("in __init__.py")
# print(myGame.gameAlphabets)
# New game
# myGame.select_random_word(myDictionary)
# print(myGame.gameAlphabets)



def create_app(config_class=Config):
    
    app = Flask(__name__)
    
    app.myDictionary = loadDictionary()
    app.myGame = setUpGame(app.myDictionary.dictionaryWords)
    
    app.config.from_object(config_class)

    moment.init_app(app)

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

