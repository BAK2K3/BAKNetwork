####################
###CORE VIEWS.PY####
####################

from baknetworks import APP_ROOT
from flask import render_template, Blueprint, send_file, redirect
from flask_login import login_required, current_user
import os

#Configure blueprint for core routes
core = Blueprint('core',__name__)

#Index Routing
@core.route('/')
def index():
    return render_template('index.html')

#DevDiary Routing
@core.route('/devdiary')
def devdiary():
    return render_template('devdiary.html')

#Contact Routing
@core.route('/contact')
def contact():
    return render_template('contact.html')

#Privacy Page Routing
@core.route('/privacy')
def privacy():
    return render_template('privacy.html')

#Database Routeing
@core.route('/database')
@login_required
def send_database():
    #Checks logged in user, and permits download of database if current user is admin.
    if current_user.email == "benjamin.a.kavanagh@gmail.com":
        filename = 'data.sqlite'
        filepath = os.path.join(APP_ROOT, filename)
        return send_file(filepath, as_attachment=True)
    #Else re-routes to index 
    else:
        return redirect (url_for('core.index'))
