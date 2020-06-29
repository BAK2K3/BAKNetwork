##BAKNETWORKS __INIT__.py##
###########################

import os

#Testing only
#os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = 'true'
port = int(os.environ.get("PORT", 5000))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_dance.contrib.google import make_google_blueprint, google
from flask_login import LoginManager
from flask_talisman import Talisman
import functools


###FLASK SETUP###
app = Flask(__name__)
app.static_folder = 'static'
app.config['PREFERRED_URL_SCHEME'] = 'https'


#Dev
#app.config.from_json('config.json')
#Deploy
app.secret_key = os.environ.get('SECRET_KEY', None)

##Set up FLASK HTTPS security
csp = {
    'default-src': [
        '\'self\'',
        'stackpath.bootstrapcdn.com',
        'code.jquery.com',
        'cdn.jsdelivr.net'
    ]
}
talisman = Talisman(app, content_security_policy=csp)
url_for = functools.partial(Flask.url_for, _scheme='https')

def _force_https():
    # my local dev is set on debug, but on AWS it's not (obviously)
    # I don't need HTTPS on local, change this to whatever condition you want.
    if not app.debug: 
        from flask import _request_ctx_stack
        if _request_ctx_stack is not None:
            reqctx = _request_ctx_stack.top
            reqctx.url_adapter.url_scheme = 'https'
app.before_request(_force_https)


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


