##NETWORKS VIEWS.PY##

from flask import render_template, request, Blueprint, flash, redirect, url_for
from flask_login import login_required, current_user, login_manager
from baknetworks.comment.forms import CommentForm 
from baknetworks.models import Comment
from baknetworks.networks.forms import RNNForm
from baknetworks import db
from baknetworks.networks.predictions import prepare_network, generate_text
# from sqlalchemy import desc

networks = Blueprint('networks',__name__)


#CNN Route
@networks.route('/cnn', methods=['GET', 'POST'])
@login_required
def cnn():

    # Comment Form
    commentform = CommentForm()
    if commentform.validate_on_submit():
        savecomment = Comment(text=commentform.text.data,
                            user_id=current_user.id,
                            page='cnn')
        db.session.add(savecomment)
        db.session.commit()
        return redirect(url_for('networks.cnn'))
    
    commentquery = Comment.query.filter_by(page='cnn').all()

    return render_template('cnn.html', commentform=commentform, commentquery=commentquery)




#RNN Route
@networks.route('/rnn/')
@login_required
def rnn_root():
    return render_template('rnn.html')

#Shakesbot Route
@networks.route('/rnn/shakesbot', methods=['GET', 'POST'])
@login_required
def rnn_shake():

    # RNN Form
    rnnform = RNNForm(prefix='a')
    # Comment Form
    commentform = CommentForm(prefix='b')

    rnnoutput=False

    
    if commentform.submit.data and commentform.validate():
        savecomment = Comment(text=commentform.text.data,
                            user_id=current_user.id,
                            page='rnn_shake')       
        db.session.add(savecomment)
        db.session.commit()
        return redirect(url_for('networks.rnn_shake'))

    if rnnform.submitrnn.data and rnnform.validate():

        start_seed = rnnform.textrnn.data
        gen_size = 500
        temp = rnnform.temprnn.data/100
        filename='shakespeare'

        rnnoutput = generate_text(start_seed, gen_size, temp, filename)
                
        commentquery = Comment.query.filter_by(page='rnn_shake').all()
        return render_template('rnn_shake.html', commentform=commentform, commentquery=commentquery, rnnform=rnnform, rnnoutput=rnnoutput)
    
  
    
    commentquery = Comment.query.filter_by(page='rnn_shake').all() 
    return render_template('rnn_shake.html', commentform=commentform, commentquery=commentquery, rnnform=rnnform)

 
#Tolstoy Route
@networks.route('/rnn/tolstoybot', methods=['GET', 'POST'])
@login_required
def rnn_tolstoy():

   # RNN Form
    rnnform = RNNForm(prefix='a')

    # Comment Form
    commentform = CommentForm(prefix='b')

    rnnoutput=False


    if commentform.submit.data and commentform.validate():
        savecomment = Comment(text=commentform.text.data,
                            user_id=current_user.id,
                            page='rnn_tolstoy')       
        db.session.add(savecomment)
        db.session.commit()
        return redirect(url_for('networks.rnn_tolstoy'))

    if rnnform.submitrnn.data and rnnform.validate():

        start_seed = rnnform.textrnn.data
        gen_size = 500
        temp = 1
        filename='tolstoybot'

        rnnoutput = generate_text(start_seed, gen_size, temp, filename)
        
        commentquery = Comment.query.filter_by(page='rnn_tolstoy').all()
        return render_template('rnn_tolstoy.html', commentform=commentform, commentquery=commentquery, rnnform=rnnform, rnnoutput=rnnoutput)
    

    
    
    commentquery = Comment.query.filter_by(page='rnn_tolstoy').all()
    return render_template('rnn_tolstoy.html', commentform=commentform, commentquery=commentquery, rnnform=rnnform)


#GAN Route
@networks.route('/gan', methods=['GET', 'POST'])
@login_required
def gan():
    
    # Comment Form
    commentform = CommentForm(prefix='a')
    if commentform.validate_on_submit():
        savecomment = Comment(text=commentform.text.data,
                            user_id=current_user.id,
                            page='gan')       
        db.session.add(savecomment)
        db.session.commit()
        return redirect(url_for('networks.gan'))

    commentquery = Comment.query.filter_by(page='gan').all()
    return render_template('gan.html', commentform=commentform, commentquery=commentquery)