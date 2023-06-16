from flask import Flask, request, jsonify
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np


app = Flask(__name__)
model_path = 'TravelLens.h5'
model = load_model(model_path)
labels = ["Bedugul",
          "Garuda Wisnu Kencana",
          "Ground Zero",
          "Monumen Bajra Sandi",
          "Patung Dewa Ruci",
          "Patung Nakula Sadewa",
          "Patung Satria Gatotkaca",
          "Tanah Lot",
          "Vihara Dharma Giri"]

@app.route('/')
def home():
    return 'Welcome to the Home Page!'

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400
    
    image = request.files['image']
    if image.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    image.save('temp.jpg')
    img = Image.open('temp.jpg')
    img = img.resize((224, 224))
    img_array = img_to_array(img)
    img_array = img_array.reshape((1, 224, 224, 3))
    img_array = img_array.astype('float32') / 255.0

    pred = model.predict(img_array)
    predicted_index = np.argmax(pred)
    predicted_label = labels[predicted_index]
    
    os.remove('temp.jpg')
    
    return jsonify({'predicted_label': predicted_label})

if __name__ == '__main__':
    app.run(debug=True)
