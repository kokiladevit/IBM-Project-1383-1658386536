import requests
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd
import tensorflow as tf
from flask import Flask, request, render_template, redirect, url_for
import os
from werkzeug.utils import secure_filename
from tensorflow.python.keras.backend import set_session

app = Flask(_name_)
model1 = load_model("fruit.h5")
model = load_model("vegetable.h5")


@app.route('/')
def home():
    return render_template('register.html')


@app.route('/result')
def result():
    return render_template('result.html')


@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        f = request.files['image']
        basepath = os.path.dirname(_file_)
        file_path = os.path.join(basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        img = image.load_img(file_path, target_size=(128, 128))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        plant = request.form['plant']
        print(plant)
        if (plant == "vegetable"):
            preds = model.predict_classes(x)
            print(preds)
            df = pd.read_excel('precautions-veg.xlsx')
            print(df.iloc[preds[0]]['caution'])
        else:
            preds = model1.predict_classes(x)

            df = pd.read_excel('precautions-fruits.xlsx')
            print(df.iloc[preds[0]]['caution'])
        return df.iloc[preds[0]]['caution']

from flask import Flask,render_template

app=Flask(__name__)

@app.route('/')
@app.route('/register')
def home():
    return render_template('register.html')

if __name__ == "__main__":
        app.run(debug=True)
