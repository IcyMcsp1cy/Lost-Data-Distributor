from flask import flash
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField,
    SubmitField,
    ValidationError)
from wtforms.validators import DataRequired, Email

from .extensions import collection

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('')


class RegistrationForm(FlaskForm):
    firstName = StringField('First name', validators=[DataRequired()])
    lastName = StringField('Last name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    institution = StringField('Institution', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = collection('user').find_one({"email": email.data})
        flash('Email Already Registered')
        if user is not None:
            raise ValidationError
        return True


class ChangeEmailForm(FlaskForm):
    old = StringField('Old Email', validators=[DataRequired(), Email()])
    e_new = StringField('New Email', validators=[DataRequired(), Email()])
    submit = SubmitField('')

    def validate_old(self, old):
        if current_user.email != old.data:
            raise ValidationError
        oldEmail = collection('user').find_one({"email": old.data})
        if oldEmail is None:
            raise ValidationError
        return True


    def validate_new(self, e_new):
        newEmail = collection('user').find_one({"email": e_new.data})
        if newEmail is not None:
            raise ValidationError
        return True


class ChangeInstitutionForm(FlaskForm):
    i_new = StringField('New Institution', validators=[DataRequired()])
    submit = SubmitField('')


class ForgotForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('')

