import joblib
import pandas as pd
import os
import sys
import json
import numpy as np
from flask import Flask, jsonify, request

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

app = Flask(__name__)
app.json_encoder = NpEncoder
global meumodelo

def init():
    print(f"Python version: {sys.version}")
    #nltk.download("punkt")
    global meumodelo
    #sess = onnxruntime.InferenceSession(
    #    os.path.join(os.getenv("AZUREML_MODEL_DIR"), "model.onnx")
    #)
    #model_path = Model.get_model_path("knn")
    #print("Model Path is  ", model_path)
    #model = joblib.load(model_path)

    #meumodelo = joblib.load( './nome_arquivo.pkl')
    modelo_name = "___MODEL_NAME___"
    print(f"Nome do Modelo: {modelo_name}")
    modelo_path = './modelo/' + modelo_name + '.pkl'
    print(f"Path do Modelo: {modelo_path}")
    meumodelo = joblib.load(modelo_path)

def run(data):
    print(data)

    json_ = json.loads(data)
    campos = pd.DataFrame(json_)

    if campos.shape[0] == 0:
        return "Dados de chamada da API estão incorretos.", 400

    for col in meumodelo.independentcols:
        if col not in campos.columns:
            campos[col] = 0
    x = campos[meumodelo.independentcols]

    prediction = meumodelo.predict(x)
    proba = None
    try:
      predict_proba = meumodelo.predict_proba(x)
      proba = list(predict_proba)
    except Exception as ex:
        print(ex)
        predict_proba = None

    ret = json.dumps({'prediction': list(prediction),
                      'proba': proba,
                      'author': "Tiago Bertoni Scarton"}, cls=NpEncoder)

    return app.response_class(response=ret, mimetype='application/json')

