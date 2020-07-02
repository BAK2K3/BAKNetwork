##Predictions.py in Networks##

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
# from PIL import Image
import tensorflow as tf
from flask import url_for, current_app
import numpy as np
import os

#Function for preparing data depending on RNN Chosen
def prepare_network(filename):
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
def generate_text(start_seed,num_generate=500,temperature, filename):

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
    
    #return the initial input, concatenated with the generated text. 
    return(start_seed+"".join(text_generated))

#Function for passing image into COVID detector
def detect_covid(input_image):

    #Load model from correct filepath
    model = load_model(os.path.join(current_app.root_path, "static/models/covid_detector.h5"), compile=False)
    
    #Convert uploaded image in PIL format
    input_image = image.load_img(input_image,target_size=(512,512,3))
    
    #Convert PIL image to array
    input_image = image.img_to_array(input_image)
    
    #Expand dimensions of array
    input_image = np.expand_dims(input_image, axis=0)
    
    #Pass array into model for classification
    predictions = model.predict(input_image)

    #return classification prediction
    return predictions