from json import dumps, loads
from . import *
from .strings import *


def test_clickdata(server):
    with server.test_client() as client:
        with server.app_context():
            response = client.post('/data/_dash-update-component', data=dumps(click_1d), content_type='application/json')
            assert response.status_code == 200
            
            response = client.post('/data/_dash-update-component', data=dumps(click_2d), content_type='application/json')
            assert response.status_code == 200

def test_download(server):
    with server.test_client() as client:
        with server.app_context():
            response = client.post('/data/_dash-update-component', data=dumps(down_rv), content_type='application/json')
            print(loads(response.get_data()))
            assert response.status_code == 200
            response = client.post('/data/_dash-update-component', data=dumps(down_1d), content_type='application/json')
            assert response.status_code == 200
            response = client.post('/data/_dash-update-component', data=dumps(down_2d), content_type='application/json')
            assert response.status_code == 200