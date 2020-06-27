##Predictions.py in Networks##

from tensorflow.keras.models import load_model
import tensorflow as tf
from flask import url_for, current_app
import numpy as np
import os
from tensorflow.keras.losses import sparse_categorical_crossentropy

# flower_model = load_model("final_iris_model.h5")


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping



def create_shakesbot(vocab_size, embed_dim,rnn_neurons, batch_size):
    model = Sequential()
    model.add(Embedding(vocab_size, embed_dim, batch_input_shape=[batch_size,None]))
    model.add(LSTM(rnn_neurons, return_sequences=True,
                 stateful=True, recurrent_initializer='glorot_uniform'))
    model.add(Dropout(0.2))
    model.add(Dense(vocab_size))
    model.compile('adam', loss=sparse_cat_loss)
    return model



def prepare_network(filename):
    path_to_file = os.path.join(current_app.root_path, "static\shakesbot", filename+"".join('.txt'))
    text = open(path_to_file, 'r', encoding='utf-8').read()
    vocab = sorted(set(text))
    char_to_ind = {char:ind for ind, char in enumerate(vocab)}
    ind_to_char = np.array(vocab)
    return char_to_ind, ind_to_char

def sparse_cat_loss(y_true,y_pred):
    return sparse_categorical_crossentropy(y_true, y_pred, from_logits=True)

def generate_text(model_create, start_seed,gen_size=500,temp=1, filename='shakespeare'):

    physical_devices = tf.config.list_physical_devices('GPU')
    tf.config.experimental.set_memory_growth(physical_devices[0], enable=True)


    filepath = os.path.join(current_app.root_path, "static\shakesbot", filename+"".join('.h5'))
   

    model = model_create(vocab_size=84,embed_dim=64, rnn_neurons=1026, batch_size=1)

    model.load_weights(filepath)

    model.build(tf.TensorShape([1,None]))

    char_to_ind, ind_to_char = prepare_network(filename)

    num_generate = gen_size
    
    input_eval = [char_to_ind[s] for s in start_seed]
    
    input_eval = tf.expand_dims(input_eval, 0)
    
    text_generated = []
    
    temperature = temp
    
    model.reset_states()
    
    for i in range(num_generate):
        
        predictions = model(input_eval)
        
        predictions = tf.squeeze(predictions,0)
        
        predictions = predictions/temperature
        
        predicted_id = tf.random.categorical(predictions, num_samples=1)[-1,0].numpy()
        
        input_eval = tf.expand_dims([predicted_id], 0)
        
        text_generated.append(ind_to_char[predicted_id])
        
    return(start_seed+"".join(text_generated))