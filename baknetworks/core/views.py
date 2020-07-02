##CORE VIEWS.PY##

from baknetworks.models import User
from flask import render_template, request, Blueprint, redirect, url_for, send_file
from flask_login import login_required, current_user, login_manager

core = Blueprint('core',__name__)



@core.route('/')
def index():

    return render_template('index.html')

@core.route('/devdiary')
def devdiary():
    return render_template('devdiary.html')

@core.route('/contact')
def contact():

    return render_template('contact.html')

@core.route('/privacy')
def privacy():

    return render_template('privacy.html')

@core.route('/database')
@login_required
def send_database():
    if current_user.email == "benjamin.a.kavanagh@gmail.com":
        filename = 'data.sqlite'
        filepath = os.path.join(APP_ROOT, filename)
        return send_file(filepath, as_attachment=True)
    else:
        return render_template('index.html')
