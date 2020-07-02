from flask import Blueprint, flash
from flask_dance.contrib.google import make_google_blueprint, google
from flask_login import login_user, current_user
import os

from baknetworks import core, db, app 
from baknetworks.models import User, OAuth

from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from sqlalchemy.orm.exc import NoResultFound

#Create a google blueprint, assigning client id and secret from environment variables, 
#Define required scope 
#set storage method through SQLAlchemy
google_blueprint = make_google_blueprint(client_id=os.environ.get('GOOGLE_ID', None),
                                client_secret=os.environ.get('GOOGLE_SECRET', None), 
                                offline=True,
                                scope=['openid https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email'],
                                storage=SQLAlchemyStorage(OAuth, db.session, user=current_user))


#Google OAuth verification and database entry via Flask Dance
@oauth_authorized.connect_via(google_blueprint)
def google_logged_in(blueprint, token):

    if not token: 
        flash("Failed to log in.", category="error")
        return False

    #Obtain account info
    account_info = blueprint.session.get('/oauth2/v3/userinfo')
    
    #Check ok
    assert account_info.ok, account_info.text

    #Obtain unique account ID from google
    account_info_json = account_info.json()
    provider_user_id = account_info_json['sub']
    
    #Query OAuth DB
    query = OAuth.query.filter_by(provider=blueprint.name, provider_user_id=provider_user_id)
    
    #Attempt to find existing oauth in DB 
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(provider=blueprint.name, provider_user_id=provider_user_id, token=token)
    
    #Log in existing user
    if oauth.user:
        login_user(oauth.user)
        flash("Successfuly signed in!")

    #Or Create new user and log them in
    else:

        email = account_info_json['email']        
        name = account_info_json['name']
        picture = account_info_json['picture']
        user = User(email=email, name=name, picture=picture)
        oauth.user = user
        db.session.add_all([user, oauth])
        db.session.commit()

        login_user(user)
        flash("Successfully signed in.")
    
    return False


# notify on OAuth provider error
@oauth_error.connect_via(google_blueprint)
def google_error(blueprint, message, response):
    msg = ("OAuth error from {name}! " "message={message} response={response}").format(
        name=blueprint.name, message=message, response=response
    )
    flash(msg, category="error")

