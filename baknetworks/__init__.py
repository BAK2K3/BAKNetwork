##BAKNETWORKS __INIT__.py##
###########################

import os

#Testing only
#os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = 'true'
port = int(os.environ.get("PORT", 5000))

from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_dance.contrib.google import make_google_blueprint, google
from flask_login import LoginManager
from flask_talisman import Talisman



###FLASK SETUP###
app = Flask(__name__)
app.static_folder = 'static'
app.config['PREFERRED_URL_SCHEME'] = 'https'


#Dev
#app.config.from_json('config.json')
#Deploy
app.secret_key = os.environ.get('SECRET_KEY', None)

#Set up FLASK HTTPS security
csp = {
    'default-src': [
        # '\'self\'',
        'stackpath.bootstrapcdn.com',
        'code.jquery.com',
        'cdn.jsdelivr.net'
        'fonts.googleapis.com'
        'w3.org'
    ]
}
talisman = Talisman(app, content_security_policy=csp)


class ReverseProxied(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        scheme = environ.get('HTTP_X_FORWARDED_PROTO')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)

app.wsgi_app = ReverseProxied(app.wsgi_app)



#Import Databases and User Oauth
from baknetworks.models import db, login_manager
from baknetworks.users.user_oauth import google_blueprint


####SQL Set Up####
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(google_blueprint, url_prefix="/login")

db.init_app(app)
Migrate(app,db)

###Set up log in manager###
login_manager.init_app(app)
login_manager.session_protection = "strong"


###BLUEPRINTS###
from baknetworks.core.views import core
from baknetworks.networks.views import networks
from baknetworks.error_pages.handlers import error_pages
from baknetworks.users.views import users
app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(users)
app.register_blueprint(networks)


