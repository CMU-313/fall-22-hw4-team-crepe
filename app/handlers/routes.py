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


    @app.route('/model', methods = ['POST'])
    def predict():
        data = request.form
        #use entries from the query string here but could also use json
        
        try: 
            student_id = data["student_id"]
            failures = data["failures"]
            schoolsup = data["schoolsup"]
            activities = data["activities"]
            internet = data["internet"]
            studytime = data["studytime"]
            age = data["age"]
        except KeyError:
            return "Unprocessable Entity", 422 
        query_df = pd.DataFrame({
            'student_id': pd.Series(student_id),
            'failures': pd.Series(failures),
            'schoolsup': pd.Series(schoolsup),
            'activities': pd.Series(activities),
            'internet': pd.Series(internet),
            'studytime': pd.Series(studytime),
            'age': pd.Series(age),
        })
        query = pd.get_dummies(query_df)
        prediction = clf.predict(query)
        return jsonify(np.asscalar(prediction))
