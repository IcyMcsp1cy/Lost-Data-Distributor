from flask import session
from flask_login import UserMixin
from werkzeug.security import (
    generate_password_hash, 
    check_password_hash)
from bson.objectid import ObjectId
import json
import random

from .extensions import login, JSONEncoder, collection

def generate_password(num):
    num = 12
    password = []
    for char in range(abs(num)):
        result = random.randrange(65, 117, 1)
        result += 6 if result > 90 else 0
        password.append(chr(result))
    return''.join(password)

class User(UserMixin):
    def __init__(self, 
    firstName, 
    lastName, 
    email, 
    institution,
    password,
    accountType,
    _id=None):
        self._id = str(ObjectId()) if _id is None else _id
        self.email = email
        self.firstName = firstName
        self.lastName = lastName
        self.institution = institution
        self.accountType = accountType
        self.password = password

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self._id

    def check_password(self, password_hash): #, password):\
        return password_hash == self.password
        # return check_password_hash(password_hash, password)


    def to_json(self):
        return {
            "_id": ObjectId(self._id),
            "email": self.email,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "institution": self.institution,
            "password": self.password,
            "type": self.accountType
        }

    

    @staticmethod
    def get_user(email):
        u = json.loads(JSONEncoder().encode(collection('user').find_one({"email": email})))
        if not u:
            return None
        return User(
            u['firstName'],
            u['lastName'],
            u['email'],
            u['institution'],
            u['password'],
            u['type'],
            u['_id'])


    @staticmethod
    def new_user(firstName, lastName, email, institution):

        password = generate_password(12)

        return User(
            firstName,
            lastName,
            email,
            institution,
            password,
            "unverified",)


    @login.user_loader
    def load_user(id):
        u = json.loads(JSONEncoder().encode(collection('user').find_one({"_id": ObjectId(id)})))
        if not u:
            return None
        return User(
            u['firstName'],
            u['lastName'],
            u['email'],
            u['institution'],
            u['password'],
            u['type'],
            u['_id'])

