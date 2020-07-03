####################
###USERS VIEWS.PY###
####################

from flask import  redirect, url_for, Blueprint
from flask_login import login_required, logout_user, current_user

from baknetworks import core

from baknetworks.models import User, OAuth, db

from flask_dance.consumer import oauth_authorized, oauth_error

from sqlalchemy.orm.exc import NoResultFound



users = Blueprint('users',__name__)
@users.route('/google')
def login():
    if not current_user.is_authenticated:
        return redirect(url_for('google.login'))
    
    return redirect(url_for('core.index'))

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('core.index'))

