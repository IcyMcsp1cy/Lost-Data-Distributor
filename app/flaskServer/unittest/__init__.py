import pytest
from flask import request, current_app
from .. import create_app
from ..extensions import collection, get_fs
from ..userClass import User

taken = User('taken', 'taken', 'taken@email.com', 'taken', 'taken', 'unverified')
adminUser = User('admin', 'admin', 'admin@email.com', 'lowell', 'adminpass', 'admin')
resUser = User('uno', 'dos', 'e@mail.com', 'nau', 'respass', 'researcher')
regUser = User('register', 'account', 'reg@email.com', 'reg', 'repass', 'unverified')
nonUser = User('no', 'no', 'n@o.o', 'no', 'no', 'no')

researchers = [
    User(
        'fRes'+str(num), 
        'lRes'+str(num), 
        'researcher'+str(num)+'@email.com', 
        'institution', 
        'password'+str(num), 
        'researcher') for num in range(5)
]



def clean_db():
    if 'TESTING' in current_app.config:
        if current_app.config['TESTING']:
            for tag in ['user', 'glossary', 'news', 'radialvelocity']:
                collection(tag).remove()
            for fs in ['one', 'two']:
                entries = list(get_fs(fs).find())
                for entry in entries:
                    get_fs(fs).delete(entry._id)
        else:
            print('test_config.TESTING set to False')
            raise ValueError
    else:
        print('test_config.TESTING not set')
        raise ValueError

def upload_files():
    pass

def populate_db():
    if 'TESTING' in current_app.config:
        if current_app.config['TESTING']:
            for user in [taken, adminUser, regUser]:
                collection('user').insert_one(user.to_json())
            get_fs('one').put(
                open('flaskServer/unittest/1d_test.csv', 'rb'),
                filename='12345.6789'
            )
            get_fs('one').put(
                open('flaskServer/unittest/1d_test.csv', 'rb'),
                filename='98765.4321'
            )
            get_fs('two').put(
                open('flaskServer/unittest/2d_test.csv', 'rb'),
                filename='12345.6789'
            )
            get_fs('two').put(
                open('flaskServer/unittest/2d_test.csv', 'rb'),
                filename='98765.4321'
            )
            collection('radialvelocity').insert_one(
                {
                    'FILENAME': '12345.6789',
                    'OBNM': 200000.1067,
                    'MJD': 50000.7392,
                    'V': 1000.23,
                    'PUBLIC': True,
                }
            )
            collection('radialvelocity').insert_one(
                {
                    'FILENAME': '98765.4321',
                    'OBNM': 300000.1067,
                    'MJD': 60000.7392,
                    'V': 2000.23,
                    'PUBLIC': True,
                }
            )
        else:
            print('test_config.TESTING set to False')
            raise ValueError
    else:
        print('test_config.TESTING not set')
        raise ValueError

@pytest.fixture(scope='session', autouse=True)
def server(): 
    server = create_app('unittest/test_config.py')
    with server.app_context():
        server.config['WTF_CSRF_ENABLED'] = False
        clean_db()
        populate_db()
    yield server
    # p.terminate()


