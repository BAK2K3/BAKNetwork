#############################
###ERROR_PAGES HANDLERS.PY###
#############################

from flask import Blueprint, render_template

#Set up error pages blueprints
error_pages = Blueprint('error_pages', __name__)

#404 error page
@error_pages.app_errorhandler(404)
def error_404(error):
    return render_template('error_pages/404.html'), 404

#403 error page
@error_pages.app_errorhandler(403)
def error_403(error):
    return render_template('error_pages/403.html'), 403

#401 error page
@error_pages.app_errorhandler(401)
def error_401(error):
    return render_template('error_pages/401.html'), 401
