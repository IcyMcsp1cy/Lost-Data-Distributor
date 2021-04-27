from flask import current_app
from flask_pymongo import PyMongo
from gridfs import GridFS
from flask_mail import Mail, Message
from flask_login import LoginManager
from bson.objectid import ObjectId
import json
from datetime import datetime

mongo = PyMongo()

def collection(collection):
    if not current_app.config['TESTING']:
        return mongo.db[collection]
    return mongo.db['test_' + collection]

def get_fs(collection):
    if not current_app.config['TESTING']:
        return GridFS(mongo.db, collection=collection)
    return GridFS(mongo.db, collection='test_'+collection)


mail= Mail()
login=LoginManager()
login.login_view = 'login'


def sendMail(recipient, header, body):
    mail.send(Message(header, sender=current_app.config['MAIL_USERNAME'], 
        recipients=[recipient], body=body))


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o,ObjectId) or isinstance(o, datetime):
            return str(o)
        return json.JSONEncoder.default(self,o)