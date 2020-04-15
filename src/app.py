from flask import Flask, request
from PIL import Image, ImageOps
import numpy as np

import tensorflow.keras
import argparse
import json
# Load the model
model = tensorflow.keras.models.load_model('./models/keras_model.h5')

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
# Replace this with the path to your image


app = Flask(__name__) 
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024


@app.route('/evalmask', methods=['POST'])
def detectMask():
    ## check isImage
    if not request.files['image'] : return {"error": "must have a image"}, 400
    try:
        checkImage = Image.open(request.files['image'].stream)
        if(checkImage.format!= 'JPG' and checkImage.format!='JPEG' and checkImage.format!='PNG'):
            return {"error":"image must be jpg, jpeg or png"},400
    except Exception as e:
        return {"error":"can not open image file. check your image file"},400
    

    size = (224, 224)
    
    image = ImageOps.fit(checkImage, size, Image.ANTIALIAS)
        #turn the image into a numpy array
    image_array = np.asarray(image)

    # display the resized image
    # image.show()

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    try:
        
        data[0] = normalized_image_array
    except :
        return {"error" : "not proper image"}
    # Load the image into the array

    # run the inference
    prediction = model.predict(data)
    result = {
        "no mask" :str(round(prediction[0][0],4)),
        "mask" : str(round(prediction[0][1],4)),
        "background": str(round(prediction[0][2],4)) 
    }
    return result

@app.errorhandler(413)
def request_entity_too_large(error):
    return {"error": 'File Too Large'}, 413

if __name__ == "__main__":
    app.run(debug=False, port=80, host='0.0.0.0')