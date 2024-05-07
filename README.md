Flask Tutorial

Setup:

    Virtual Environment:
        $ python3 -m venv venv
        $ venv\Scripts\activate
    
    Install flask:
        $ pip install flask
    
    Run flask:
        $ flask run
        $ flask run --port 5001
    
    Environment variables (read FLASK_APP variable from .flaskenv file)
        $ pip install python-dotenv

    Flask HTML Forms:
        $ pip install flask-wtf

    Database and migration:
        $ pip install flask-sqlalchemy          # Database Object Relational Mapper/Model ORM 
        $ pip install flask-migrate             # Database migration framework
        $ flask db init                         # Create migration repository
        $ flask db migrate -m "comments"        # Database migration; generates script; run whenever change to ORM
        $ flask db upgrade                      # Run the script to create database
        $ flask db downgrade                    # Downgrade 1 level earlier
        $ flask db downgrade base               # Wipes out to base target, i.e., blank db
    
    Python shell with flask
        $ flask shell                           # Need to set context first; app.app_context().push()

    Flask login
        $ pip import flask-login
    
    Email validator
        $ pip install email-validator

    Flask email
        $ pip install flask-mail

    JWT tokens
        $ pip install pyjwt
        
    Avatar generator
        Gravatar

    SMTP debugging server (prints to terminal)
        $ pip install aiosmtpd
        $ aiosmtpd -n -c aiosmtpd.handlers.Debugging -l localhost:8025
        
        $ set MAIL_SERVER=localhost
        $ set MAIL_PORT=8025

    Run with waitress
        $ pip install waitress
        $ waitress-serve --listen=127.0.0.1:5000 microblog:myFlask 

    CSS Bootstrap

    Browser side timezone / moment.js
        $ pip install flask-moment

    Multilanguage Internationalization I18n, Localization L10n
        $ pip install flask-babel

    Language detection
        $ pip install langdetect

    http requests
        $ pip install requests
    
    Command line http client
        $ pip install httpie