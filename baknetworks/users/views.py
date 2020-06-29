from flask import Flask, redirect, url_for, render_template, Blueprint, request, flash
from flask_dance.contrib.google import make_google_blueprint, google
from flask_login import login_required, logout_user, login_user, current_user

from baknetworks import core, app
from baknetworks.models import User, OAuth, db

from flask_dance.consumer import oauth_authorized, oauth_error

from sqlalchemy.orm.exc import NoResultFound



users = Blueprint('users',__name__)
@users.route('/google')
def login():
    if not current_user.is_authenticated:
        return redirect(url_for('google.login'))
    
    return redirect(url_for('core.about')

@users.route('/logout')
# @login_required
def logout():
    logout_user()
    return redirect(url_for('core.index'))

