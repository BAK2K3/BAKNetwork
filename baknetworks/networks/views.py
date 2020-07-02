##NETWORKS VIEWS.PY##

from flask import render_template, request, Blueprint, flash, redirect, url_for, current_app
from flask_login import login_required, current_user, login_manager
from baknetworks.comment.forms import CommentForm 
from baknetworks.models import Comment
from baknetworks.networks.forms import RNNForm
from baknetworks import db
from baknetworks.networks.predictions import prepare_network, generate_text
from werkzeug.utils import secure_filename
# from sqlalchemy import desc

networks = Blueprint('networks',__name__)


#RNN Route
@networks.route('/rnn/')
def rnn_root():
    return render_template('rnn.html')

#Shakesbot Route
@networks.route('/rnn/shakesbot', methods=['GET', 'POST'])
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


#CNN Route
@networks.route('/cnn/covid', methods=['GET', 'POST'])
def cnn_covid():

    # RNN Form
    cnnform = CNNForm(prefix='a')

    # Comment Form
    commentform = CommentForm(prefix='b')

    cnnoutput = False

    # Comment Form
    commentform = CommentForm()
    if commentform.validate_on_submit():
        savecomment = Comment(text=commentform.text.data,
                            user_id=current_user.id,
                            page='cnn_covid')
        db.session.add(savecomment)
        db.session.commit()
        return redirect(url_for('networks.cnn_covid'))


    if cnnform.submitcnn.data and cnnform.validate():

        filename = secure_filename(cnnform.filecnn.data.filename)
        cnnform.filecnn.save((os.path.join(current_app.root_path, "static/models/") + filename))

        # cnnoutput = detect_covid()
        
        commentquery = Comment.query.filter_by(page='cnn_covid').all()
        return render_template('cnn_covid.html', commentform=commentform, commentquery=commentquery, cnnform=cnnform, cnnoutput=cnnoutput)
    

    
    
    commentquery = Comment.query.filter_by(page='cnn_covid').all()

    return render_template('cnn_covid.html', commentform=commentform, commentquery=commentquery)





#CNN Route
@networks.route('/cnn')
def cnn():
    return render_template('cnn.html')

#GAN Route
@networks.route('/gan', methods=['GET', 'POST'])
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



