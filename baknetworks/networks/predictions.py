##Predictions.py in Networks##

from tensorflow.keras.models import load_model
import tensorflow as tf
from flask import url_for, current_app
import numpy as np
import os

def prepare_network(filename):
    path_to_file = os.path.join(current_app.root_path, "static\models\\", filename+"".join('.txt'))
    text = open(path_to_file, 'r', encoding='utf-8').read()
    vocab = sorted(set(text))
    char_to_ind = {char:ind for ind, char in enumerate(vocab)}
    ind_to_char = np.array(vocab)
    return char_to_ind, ind_to_char

def generate_text(start_seed,gen_size=500,temp=1, filename='shakespeare'):

    filepath = os.path.join(current_app.root_path, "static\models\\", filename+"".join('.h5'))
   
    char_to_ind, ind_to_char = prepare_network(filename)

    model = load_model(filepath, compile=False)

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