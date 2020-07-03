#############################
###BAKNETWORKS __INIT__.py###
#############################

import os
from flask import Flask
from flask_migrate import Migrate
from flask_talisman import Talisman
import gc

#configure garbabe collection
gc.enable()

# os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = 'true'

#Flask Setup
app = Flask(__name__)
app.static_folder = 'static'
app.config['PREFERRED_URL_SCHEME'] = 'https'
app.secret_key = os.environ.get('SECRET_KEY', None)

#Define Root folder location
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

#Set up Content Security Policy 
csp = {
    'default-src': [
         '\'self\'',
        'stackpath.bootstrapcdn.com',
        'code.jquery.com',
        'cdn.jsdelivr.net',
        '*.googleapis.com',
        '*.gstatic.com',
        'w3.org'
    ],
    'script-src': [
        '\'self\'',
        '\'sha256-hiwDPNhsIbfBqHeUAiBkfuGzaQAWxVx1sIFuSOA/A3M=\'',
        '\'sha256-km/e8rf92a5m6UdebHyfOamTMnsk/gCqVP1QCBMQqpI=\'',
        'cdn.jsdelivr.net',
        'code.jquery.com',
        'stackpath.bootstrapcdn.com',       
    ],
    'img-src': [
        '\'self\'',
        '*.googleusercontent.com',
        'w3.org',
        "data:"
    ]
}

#Set up Talisman 
talisman = Talisman(app, content_security_policy=csp)

#Set up internal redirects to be HTTPS for OAuth
class ReverseProxied(object):
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):
        scheme = environ.get('HTTP_X_FORWARDED_PROTO')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)
app.wsgi_app = ReverseProxied(app.wsgi_app)

#Import Database Models and Google User Oauth blueprint
from baknetworks.models import db, login_manager
from baknetworks.users.user_oauth import google_blueprint

#SQL Set Up
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Register Google OAuth blueprint
app.register_blueprint(google_blueprint, url_prefix="/login")

#Connect database
db.init_app(app)
Migrate(app,db)

#Set up log in manager
login_manager.init_app(app)
login_manager.session_protection = "strong"

#Routing blueprint importing and registering
from baknetworks.core.views import core
from baknetworks.networks.views import networks
from baknetworks.error_pages.handlers import error_pages
from baknetworks.users.views import users
app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(users)
app.register_blueprint(networks)
