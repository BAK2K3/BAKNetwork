##CORE VIEWS.PY##

from baknetworks.models import User
from flask import render_template, request, Blueprint, redirect, url_for
from flask_login import login_required, current_user, login_manager

core = Blueprint('core',__name__)



@core.route('/')
def index():

    if current_user.is_authenticated:
        return redirect(url_for('core.about'))

    return render_template('index.html')

@core.route('/about')
@login_required
def about():
    return render_template('about.html')

@core.route('/contact')
@login_required
def contact():

    return render_template('contact.html')

@core.route('/privacy')
def privacy:

    return render_template('privacy.html')