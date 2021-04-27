from . import *
from ..userClass import User


def test_index(server):
    with server.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200

def test_not_found(server):
    with server.test_client() as client:
        response = client.get('/obviouslyFake')
        assert response.status_code == 404

def test_admin(server):
    with server.test_client() as client:
        response = client.get('/admin/')
        assert response.status_code == 302

        client.post('/login', data=dict(
                email='taken@email.com', 
                password='taken',
        ))
        response = client.get('/admin/')
        assert response.status_code == 403

        client.get('/logout')
        client.post('/login', data=dict(
                email='admin@email.com', 
                password='adminpass',
        ))
        response = client.get('/admin/')
        assert response.status_code == 200

def test_login(server):
    with server.test_client() as client:
        with server.app_context():
            response = client.get('/login')
            assert response.status_code == 200

            response = client.post('/login', data=dict(email='no', password='no'))
            assert response.status_code == 200

            response = client.post('/login', data=dict(email='taken@email.com', password='taken'))
            assert response.location == 'http://localhost/'


def test_logout(server):
    with server.test_client() as client:
        with server.app_context():
            response = client.get('/logout')
            assert response.status_code == 302

            response = client.post('/login', data=dict(
                email='taken@email.com', 
                password='taken',
            ))
            assert response.location == 'http://localhost/'

            response = client.get('/logout')
            assert response.status_code == 302

            response = client.get('/login')
            assert response.status_code == 200

            response = client.get('/admin/')
            assert response.status_code == 302


def test_register(server):
    with server.test_client() as client:
        with server.app_context():
            response = client.get('/register')
            assert response.status_code == 200

            response = client.post('/register', data=dict(
                firstName='register', 
                lastName='test', 
                email='taken@email.com', 
                institution='lowell',
                ))
            assert response.status_code == 200


            response = client.post('/register', data=dict(
                firstName='register', 
                lastName='test', 
                email='regtest@email.com', 
                institution='lowell',
                ))
            assert response.location == 'http://localhost/'

            entry = collection('user').find_one({'email': 'regtest@email.com'})
            assert entry is not None


def test_account(server):
    with server.test_client() as client:
        with server.app_context():
            response = client.get('/account')
            assert response.status_code == 403

            response = client.post('/login', data=dict(
                email='taken@email.com', 
                password='taken',
            ))

            response = client.get('/account')
            assert response.status_code == 200

            response = client.post('/account', data=dict(
                old='taken@email.com', 
                e_new='something@else.com',
                ))
            assert response.status_code == 200

            entry = collection('user').find_one({'email': 'taken@email.com'})
            assert entry is None

            response = client.post('/account', data=dict(
                old='something@else.com',
                e_new='taken@email.com', 
                ))
            assert response.status_code == 200

            entry = collection('user').find_one({'email': 'taken@email.com'})
            assert entry is not None

            response = client.post('/account', data=dict(
                i_new='new', 
                ))
            assert response.status_code == 200

            entry = collection('user').find_one({'email': 'taken@email.com'})
            assert entry['institution'] == 'new'
            client.post('/account', data=dict(
                i_new='taken', 
                ))

def test_forgot(server):
    with server.test_client() as client:
        with server.app_context():
            response = client.get('/forgot')
            assert response.status_code == 200

            response = client.post('/forgot', data=dict(
                email='not@there.com', 
            ))
            assert response.location == 'http://localhost/register'

            response = client.post('/forgot', data=dict(
                email='taken@email.com', 
            ))
            assert response.location == 'http://localhost/login'

            response = client.post('/login', data=dict(
                email='taken@email.com', 
                password='taken',
            ))

            response = client.get('/forgot')
            assert response.location == 'http://localhost/'

def test_news(server):
    with server.test_client() as client:
        with server.app_context():
            response = client.get('/news')
            assert response.status_code == 200

            entries = collection('news').find()
            for entry in entries:
                response = client.get('/post/'+str(entry['_id']))
            assert response.status_code == 200

def test_glossary(server):
    with server.test_client() as client:
        with server.app_context():
            response = client.get('/glossary')
            assert response.status_code == 200
