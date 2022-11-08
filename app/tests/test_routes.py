import json
from flask import Flask

from app.handlers.routes import configure_routes

def test_base_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/'

    response = client.get(url)

    assert response.status_code == 200
    assert response.get_data() == b'try the predict route it is great!'

def test_model_retrieved():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/model'
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.data, bytes)

def test_output_types():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/model'
    
    data = json.dumps({
        "failures": 0, 
        "schoolsup": True, 
        "internet": True,
        "studytime": 0.0,
        "absences": 0,
        "Medu": 0,
        "Fedu": 0,
        "paid": True,
        "famsup": True
    })

    response = client.post(url,json = data)
    
    assert response.status_code == 200
    assert len(response.data) == 3
    assert all(isinstance(elem, str) for elem in response.data)

def test_post_422():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/model'
    
    data = json.dumps({
        "student_id": 0,
        "failures": 0,
        "schoolsup": True,
        "activities": True,
        "internet": True,
        "studytime": 0,
    })

    response = client.post(url,json=data)
    assert response.status_code == 422
    
def test_post_model_route_422_wrong_type():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/model'
    data = json.dumps({
        "student_id": 0,
        "failures": 0,
        "schoolsup": True,
        # Wrong type 
        "activities": 3,
        "internet": True,
        "studytime": 0,
        "age": 0
    })
    
    response = client.post(url, json=data)
    
    assert response.status_code == 422 
