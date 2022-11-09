import pickle
import this
import json
from flask import Flask, jsonify, request
import joblib
import pandas as pd
import numpy as np
import os

def configure_routes(app):

    this_dir = os.path.dirname(__file__)
    model_path = os.path.join(this_dir, "model.pkl")
    clf = joblib.load(model_path)

    @app.route('/')
    def hello():
        return "try the predict route it is great!"

    @app.route('/model', methods = ['GET'])
    def getModel():
        with open(model_path, "rb") as pickle_file:
            data = pickle_file.read()
            response = app.make_response(data) 
            response.content_type = "application/octet-stream"
            return response 

    @app.route('/model', methods = ['POST'])
    def predict():
        data = json.loads(request.json)
        # Expected Keys
        predict_schema = {
            "failures": int, 
            "schoolsup": bool, 
            "internet": bool,
            "studytime": float,
            "absences": int,
            "Medu": int,
            "Fedu": int,
            "paid": bool,
            "famsup": bool
        }
        try:
            predict_dict = {k:data[k] for k in predict_schema}
            for k in predict_schema:
                if not isinstance(predict_dict[k], predict_schema[k]): raise TypeError
        except (KeyError, TypeError):
            return "Unprocessable Entity", 422
        # Postprocessing
        predict_dict["schoolsup"] = int(predict_dict["schoolsup"])
        predict_dict["paid"] = int(predict_dict["schoolsup"])
        predict_dict["internet"]=int(predict_dict["internet"])
        predict_dict["famsup"]=int(predict_dict["famsup"])
         
        query_df = pd.DataFrame({k:pd.Series(v) for k,v in predict_dict.items()})
        query = pd.get_dummies(query_df)
        print(query)
        prediction = clf.predict(query)
        response = app.make_response(str(prediction[0]))
        response.content_type = "html/text; charset=utf-8"
        return response 
