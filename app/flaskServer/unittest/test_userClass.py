from bson import ObjectId
from ..userClass import User
from . import *

fName = 'first'
lName = 'last'
email = 'email@email.email'
inst = 'institution'



def test_new_user():
    '''
    GIVEN a User model
    WHEN a new User is created
    THEN check if the fields are valid
    '''
    user = User.new_user(fName, lName, email, inst)
    assert user.firstName == fName
    assert user.lastName == lName
    assert user.email == email
    assert user.institution == inst
    assert len(user.password) == 12


def test_user_mixin():
    '''
    GIVEN a valid User model
    WHEN a new User is created
    THEN check if Mixin fields are valid
    '''
    user = resUser
    assert user.is_authenticated()
    assert user.is_active()
    assert not User.is_anonymous()
    assert user.check_password(user.password)
    assert isinstance(user.to_json(), dict)


def test_get_user(server):
    with server.test_client() as client:
        with server.app_context():
            entry = collection('user').find_one({'email': 'taken@email.com'})
            user = User.get_user('taken@email.com')
            assert ObjectId(user._id) == entry['_id']