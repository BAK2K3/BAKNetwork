#######################
###NETWORKS VIEWS.PY###
#######################

from flask import render_template, Blueprint, redirect, url_for
from flask_login import current_user
from baknetworks.comment.forms import CommentForm 
from baknetworks.models import Comment
from baknetworks.networks.forms import RNNForm, CNNForm
from baknetworks import db, APP_ROOT
from baknetworks.networks.predictions import prepare_network, generate_text, detect_covid
from werkzeug.utils import secure_filename
import numpy as np
import os
import gc

#Set up Blueprint for Networks Views
networks = Blueprint('networks',__name__)

#RNN Route
@networks.route('/rnn/')
def rnn_root():
    #Run Garbage Collector
    gc.collect()
    return render_template('rnn.html')

##################################################
##################SHAKESBOT#######################
##################################################

#Shakesbot Route
@networks.route('/rnn/shakesbot', methods=['GET', 'POST'])
def rnn_shake():

    #Create an RNN Form instance
    rnnform = RNNForm(prefix='a')

    #Creete a Comment Form instance
    commentform = CommentForm(prefix='b')

    #Set default rnnoutput to False
    rnnoutput=False

    #If Comment form has been submitted
    if commentform.submit.data and commentform.validate():
        
        #Extract Comment data from form
        savecomment = Comment(text=commentform.text.data,
                            user_id=current_user.id,
                            page='rnn_shake')

        #Save and Commit Comment data to Database       
        db.session.add(savecomment)
        db.session.commit()
        return redirect(url_for('networks.rnn_shake'))

    #If RNN form has been submitted 
    if rnnform.submitrnn.data and rnnform.validate():

        #Extract RNN Form data
        start_seed = rnnform.textrnn.data
        temp = rnnform.temprnn.data/100
        filename='shakespeare'

        #Pass Form Data to Shakesbot text generation
        rnnoutput = generate_text(start_seed, temp, filename)
        
        #Filter comment data for this page
        commentquery = Comment.query.filter_by(page='rnn_shake').all()

        #Return Relevant Information to page
        return render_template('rnn_shake.html', commentform=commentform, commentquery=commentquery, rnnform=rnnform, rnnoutput=rnnoutput)
    
    #Filter comment data for this page
    commentquery = Comment.query.filter_by(page='rnn_shake').all() 
    #Return Relevant Information to page
    return render_template('rnn_shake.html', commentform=commentform, commentquery=commentquery, rnnform=rnnform)

###################################################
##################TOLSTOYBOT#######################
###################################################

#Tolstoy Route
@networks.route('/rnn/tolstoybot', methods=['GET', 'POST'])
def rnn_tolstoy():

    #Create RNN Form Instance
    rnnform = RNNForm(prefix='a')

    #Create Comment Form Instance
    commentform = CommentForm(prefix='b')

    #Set default rnnoutput to False
    rnnoutput=False

    #If Comment form has been submitted
    if commentform.submit.data and commentform.validate():

        #Extract Comment data from form
        savecomment = Comment(text=commentform.text.data,
                            user_id=current_user.id,
                            page='rnn_tolstoy')    

        #Save and Commit Comment data to Database    
        db.session.add(savecomment)
        db.session.commit()
        return redirect(url_for('networks.rnn_tolstoy'))

    #If RNN form has been submitted 
    if rnnform.submitrnn.data and rnnform.validate():

        #Extract RNN Form data
        start_seed = rnnform.textrnn.data
        temp = rnnform.temprnn.data/100
        filename='tolstoybot'
        
        #Pass Form Data to Tolstoybot text generation
        rnnoutput = generate_text(start_seed, temp, filename)
        
        #Filter comment data for this page
        commentquery = Comment.query.filter_by(page='rnn_tolstoy').all()
        #Return Relevant Information to page
        return render_template('rnn_tolstoy.html', commentform=commentform, commentquery=commentquery, rnnform=rnnform, rnnoutput=rnnoutput)
    
    #Filter comment data for this page
    commentquery = Comment.query.filter_by(page='rnn_tolstoy').all()
    #Return Relevant Information to page
    return render_template('rnn_tolstoy.html', commentform=commentform, commentquery=commentquery, rnnform=rnnform)

#CNN Route
@networks.route('/cnn')
def cnn():
    #Run Garbage Collector
    gc.collect()
    return render_template('cnn.html')

##############################################
##################COVID#######################
##############################################

#CNN Route
@networks.route('/cnn/covid', methods=['GET', 'POST'])
def cnn_covid():
    
    #Create CNN Form instance
    cnnform = CNNForm(prefix='a')

    #Create Comment Form
    commentform = CommentForm(prefix='b')

    #If Comment form has been submitted
    if commentform.validate_on_submit():

        #Extract Comment data from form
        savecomment = Comment(text=commentform.text.data,
                            user_id=current_user.id,
                            page='cnn_covid')

        #Save and Commit Comment data to Database  
        db.session.add(savecomment)
        db.session.commit()
        return redirect(url_for('networks.cnn_covid'))

    #If CNN form has been submitted 
    if cnnform.submitcnn.data and cnnform.validate():
    
        #Obtain Filename
        filename = secure_filename(cnnform.filecnn.data.filename)
        
        #Set Filepath
        filepath = os.path.join(APP_ROOT, 'static', filename)

        #Save file
        cnnform.filecnn.data.save(filepath)
        
        #Run Model, obtain prediction
        cnnoutput = detect_covid(filepath)
        
        #Set text based output Classification based on prediction
        if cnnoutput[0][0] < 0.5:
            cnnoutput = "The model has predicted this is a COVID 19 X Ray"
        else:
            cnnoutput = "The model has predicted this is a NORMAL X Ray"  

        #Remove File
        os.remove(filepath)
                       
        #Filter comment data for this page
        commentquery = Comment.query.filter_by(page='cnn_covid').all()

        #Return Relevant Information to page
        return render_template('cnn_covid.html', commentform=commentform, commentquery=commentquery, cnnform=cnnform, cnnoutput=cnnoutput)
    
    #Filter comment data for this page
    commentquery = Comment.query.filter_by(page='cnn_covid').all()

    #Return Relevant Information to page
    return render_template('cnn_covid.html', commentform=commentform, commentquery=commentquery, cnnform=cnnform)


#GAN Route
@networks.route('/gan', methods=['GET', 'POST'])
def gan():
    gc.collect()
    #Create Comment Form Instance
    commentform = CommentForm(prefix='a')

    #If Comment form has been submitted
    if commentform.validate_on_submit():

        #Extract Comment data from form
        savecomment = Comment(text=commentform.text.data,
                            user_id=current_user.id,
                            page='gan')   

        #Save and Commit Comment data to Database  
        db.session.add(savecomment)
        db.session.commit()
        return redirect(url_for('networks.gan'))

    #Filter comment data for this page
    commentquery = Comment.query.filter_by(page='gan').all()

    #Return Relevant Information to page
    return render_template('gan.html', commentform=commentform, commentquery=commentquery)

