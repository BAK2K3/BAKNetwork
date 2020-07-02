##CORE VIEWS.PY##

from baknetworks.models import User
from flask import render_template, request, Blueprint, redirect, url_for
from flask_login import login_required, current_user, login_manager

core = Blueprint('core',__name__)



@core.route('/')
def index():

    return render_template('index.html')

@core.route('/devdiary')

def about():
    return render_template('devdiary.html')

@core.route('/contact')
@login_required
def contact():

    return render_template('contact.html')

@core.route('/privacy')
def privacy():

    return render_template('privacy.html')