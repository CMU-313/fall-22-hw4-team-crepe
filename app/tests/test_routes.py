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
    assert isinstance(response, list)

def test_output_types():
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
        "school": "CMU",
        "age": 0
    })

    response = client.post(url,json = data)
    
    assert all(isinstance(elem, str) for elem in response)
    assert len(response) == 3
    assert response.status_code == 200

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
