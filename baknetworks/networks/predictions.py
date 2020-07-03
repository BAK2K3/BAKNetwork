##Predictions.py in Networks##

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

import tensorflow as tf
from flask import url_for, current_app
import numpy as np
import os


#Function for preparing data depending on RNN Chosen
def prepare_network(filename):

    """Takes in the filename of the bot, prepares and returns the relevant character index mappings"""

    #Sets filepath for the corpus of text 
    path_to_file = os.path.join(current_app.root_path, "static/models/", filename+"".join('.txt'))

    #Open Text File
    text = open(path_to_file, 'r', encoding='utf-8').read()

    #Obtain set of vocabulary
    vocab = sorted(set(text))

    #Create a character index (forwards and backwards)
    char_to_ind = {char:ind for ind, char in enumerate(vocab)}
    ind_to_char = np.array(vocab)

    #Return both mappings  
    return char_to_ind, ind_to_char


#Function for generating text from requested model
def generate_text(start_seed, temperature, filename, num_generate=500):

    """Prepares the model of name "filename", and generates "num_generate" amount of text
    from specificied model, with a probability multiplier of specificed temperature, and 
    returns the original seed and subsequently generated text."""

    #Obtain filepath for requested model
    filepath = os.path.join(current_app.root_path, "static/models/", filename+"".join('.h5'))
   
    #Obtain index mappings for requested corpus
    char_to_ind, ind_to_char = prepare_network(filename)

    #Load the correct model to memory
    model = load_model(filepath, compile=False)
    
    #Map each character in start_seed to it's relative index
    input_eval = [char_to_ind[s] for s in start_seed]
    
    #Expand the dimensions
    input_eval = tf.expand_dims(input_eval, 0)
    
    #Create empty list for generated text
    text_generated = []
    
    #Reset the states of the model        
    model.reset_states()
    
    #for each iteration of num_generate
    for i in range(num_generate):
        
        #Obtain probability matrix for current iteration 
        predictions = model(input_eval)
        
        #Reduce dimensions
        predictions = tf.squeeze(predictions,0)

        #Multiply probability matrix by temperature
        predictions = predictions/temperature
        
        #Select a random outcome, based on the unnormalized log-probabilities produced by the model
        predicted_id = tf.random.categorical(predictions, num_samples=1)[-1,0].numpy()
        
        #Expand dimensions of prediction and assign as next input evaluation
        input_eval = tf.expand_dims([predicted_id], 0)
        
        #Convert prediction to char and append to generated list of text
        text_generated.append(ind_to_char[predicted_id])
    
    #Destroys model from memory
    tf.compat.v1.reset_default_graph()
    tf.keras.backend.clear_session()
    del model
    
    #return the initial input, concatenated with the generated text. 
    return(start_seed+"".join(text_generated))

#Function for passing image into COVID detector
def detect_covid(input_image):

    """Takes in filepath of image, converted it to a PIL, reshape and scale appropriately, 
    feeds to model to obtain a prediction, and returns classifier of 0 (COVID) or 1 (Normal) """

    #Load model from correct filepath
    model = load_model(os.path.join(current_app.root_path, "static/models/covid_detector.h5"), compile=False)
    
    #Convert uploaded image in PIL format
    input_image = image.load_img(input_image,target_size=(512,512,3))
    
    #Convert PIL image to array
    input_image = image.img_to_array(input_image)
    
    #Expand dimensions of array
    input_image = np.expand_dims(input_image, axis=0)

    #Scale image
    input_image = input_image/255
    
    #Pass array into model for classification
    predictions = model.predict(input_image)

    #Destroys model from memory
    tf.compat.v1.reset_default_graph()
    tf.keras.backend.clear_session()
    del model

    #return classification prediction
    return predictions