##BAKNETWORKS MODELS.PY##


from datetime import datetime
from flask_login import UserMixin, current_user, LoginManager
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin, SQLAlchemyStorage
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(UserMixin, db.Model):

 
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    picture = db.Column(db.String(200))

    posts = db.relationship('Comment', backref='author', lazy=True)

    def __repr__(self):
        return f"The current user is {self.name}"
    

    # active = db.Column(db.Boolean, default=False)
    # tokens = db.Column(db.Text)
    # created_at = db.Column(db.DateTime, default=datetime.datetime.bstnow())


class OAuth(OAuthConsumerMixin, db.Model):

    provider_user_id = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User)

    
class Comment(db.Model):

    __tablename__ = "comments"

    users = db.relationship(User)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    text = db.Column(db.Text, nullable=False)
    page = db.Column(db.String(20), nullable=False)

    def __init__(self,text,user_id,page):
       
        self.text = text
        self.user_id = user_id
        self.page = page

    def __repr__(self):
        return f"Post ID: {self.id}"
   


## CNNHistory
## RNNHistory
## GANHistory


login_manager = LoginManager()
#login_manager.login_view = "google.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

