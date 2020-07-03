####################
###USERS VIEWS.PY###
####################

from flask import  redirect, url_for, Blueprint
from flask_login import login_required, logout_user, current_user

# Set up users blueprint
users = Blueprint('users',__name__)

#Log in route
@users.route('/google')
def login():
    if not current_user.is_authenticated:
        return redirect(url_for('google.login'))
    return redirect(url_for('core.index'))

#Log out route
@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('core.index'))

