import pickle
import this
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
        pickle_file = open("model.pkl", "r")
        encrypted_list = pickle.load(pickle_file)
        return encrypted_list

    @app.route('/model', methods = ['POST'])
    def predict():
        data = request.json
        # Expected Keys
        predict_schema = {
            "student_id": int, 
            "failures": int, 
            "schoolsup": bool, 
            "activities": bool, 
            "internet": bool,
            "studytime": float,
            "age": int
        }
        try: 
            predict_dict = {k:data[k] for k in predict_schema}
            for k in predict_schema:
                if not isinstance(predict_dict[k], predict_schema[k]): raise TypeError
        except (KeyError, TypeError):
            return "Unprocessable Entity", 422 
        query_df = pd.DataFrame({k:pd.Series(v) for k,v in predict_dict.items()})
        query = pd.get_dummies(query_df)
        prediction = clf.predict(query)
        return jsonify(np.asscalar(prediction))
