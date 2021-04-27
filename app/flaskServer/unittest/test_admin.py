from json import dumps, loads
from . import *
from .strings import *


def test_news(server):
    with server.test_client() as client:
        with server.app_context():
            client.post('/login', data=dict(
                email='admin@email.com', 
                password='adminpass',
            ))
            response = client.post('/admin/_dash-update-component', data=dumps(news_submit), content_type='application/json')
            post = collection('news').find_one({'title': 'title'})
            assert post is not None

            response = client.post('/admin/_dash-update-component', data=dumps(news_select(post)), content_type='application/json')
            assert loads(response.get_data()) == news_select_res

            response = client.post('/admin/_dash-update-component', data=dumps(news_home(post)), content_type='application/json')
            assert loads(response.get_data()) == news_home_res(post)



def test_user(server):
    with server.test_client() as client:
        with server.app_context():
            client.post('/login', data=dict(
                email='admin@email.com', 
                password='adminpass',
            ))
            response = client.post('/admin/_dash-update-component', data=dumps(user_select), content_type='application/json')
            assert loads(response.get_data()) == user_select_res

            response = client.post('/admin/_dash-update-component', data=dumps(user_display), content_type='application/json')
            assert loads(response.get_data()) == user_display_res

            response = client.post('/admin/_dash-update-component', data=dumps(user_reject), content_type='application/json')
            user = collection('user').find_one({'fName': 'taken'})

            assert user is None

            response = client.post('/admin/_dash-update-component', data=dumps(user_verify), content_type='application/json')
            user = list(collection('user').find({}))

            assert len(user) == 1


def test_glossary(server):
    with server.test_client() as client:
        with server.app_context():
            client.post('/login', data=dict(
                email='admin@email.com', 
                password='adminpass',
            ))
            response = client.post('/admin/_dash-update-component', data=dumps(glos_submit), content_type='application/json')
            post = collection('glossary').find_one({'entry': 'term'})
            assert post is not None

            print(loads(response.get_data()))
            assert loads(response.get_data()) == glos_submit_res(post)

            response = client.post('/admin/_dash-update-component', data=dumps(glos_delete(post)), content_type='application/json')
            assert loads(response.get_data()) == glos_delete_res


def test_file(server):
    with server.test_client() as client:
        with server.app_context():
            client.post('/login', data=dict(
                email='admin@email.com', 
                password='adminpass',
            ))
            response = client.post('/admin/_dash-update-component', data=dumps(date_submit("2020-11-01")), content_type='application/json')
            assert loads(response.get_data()) == date_submit_res

            rv = list(collection('radialvelocity').find())
            assert rv[0]['PUBLIC'] == True
            assert rv[1]['PUBLIC'] == False

            response = client.post('/admin/_dash-update-component', data=dumps(date_submit("2019-11-01")), content_type='application/json')




