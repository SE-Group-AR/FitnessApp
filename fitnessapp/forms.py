
"""
Copyright (c) 2024 Arkoh Lawrence, Lingjun Liu, Habib Mohammed
This code is licensed under MIT license (see LICENSE for details)

@author: ENERGIZE


This python file is used in and is part of the ENERGIZE project.

For more information about the ENERGIZE project, visit:
https://github.com/CSC510-GROUP-40/FitnessApp

"""
# from datetime import date
# from re import sub
# from flask import app
"""Importing modules to create forms"""


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.core import DateField, SelectField, TimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .apps import App
import logging
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class RegistrationForm(FlaskForm):
    """Form to collect the registration data of the user"""
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[
            DataRequired(), EqualTo('password')])
    weight = StringField(
        'Weight', validators=[
            DataRequired(), Length(
                min=2, max=20)])
    height = StringField(
        'Height', validators=[
            DataRequired(), Length(
                min=2, max=20)])
    goal = StringField(
        'Goal (Weight Loss/ Muscle Gain)', validators=[
            DataRequired(), Length(
                min=2, max=20)])
    target_weight = StringField(
        'Target Weight', validators=[
            DataRequired(), Length(
                min=2, max=20)])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        """Function to validate the entered email"""
        app_object = App()
        mongo = app_object.mongo

        temp = mongo.db.user.find_one({'email': email.data}, {'email', 'pwd'})
        if temp:
            raise ValidationError('Email already exists!')


class LoginForm(FlaskForm):
    """Login form to log in to the application"""
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')



class CalorieForm(FlaskForm):
    """Form to rcord the calorie intake details of the user"""
    app = App()
    mongo = app.mongo

    cursor = mongo.db.food.find()
    get_docs = []
    for record in cursor:
        get_docs.append(record)

    result = []
    temp = ""
    for i in get_docs:
        temp = i['food'] + ' (' + i['calories'] + ')'
        result.append((temp, temp))

    food = SelectField(
        'Select Food', choices=result)

    ENERGIZE = StringField('Burn Out', validators=[DataRequired()])
    submit = SubmitField('Save')


class UserProfileForm(FlaskForm):
    """Form to input user details to store their height, weight, goal and target weight"""
    weight = StringField(
        'Weight', validators=[
            DataRequired(), Length(
                min=2, max=20)])
    height = StringField(
        'Height', validators=[
            DataRequired(), Length(
                min=2, max=20)])
    goal = StringField(
        'Goal (Weight Loss/ Muscle Gain)', validators=[
            DataRequired(), Length(
                min=2, max=20)])
    target_weight = StringField(
        'Target Weight', validators=[
            DataRequired(), Length(
                min=2, max=20)])
    submit = SubmitField('Update')


class HistoryForm(FlaskForm):
    """Form to input the date for which the history needs to be displayed"""
    app = App()
    mongo = app.mongo
    date = DateField()
    submit = SubmitField('Fetch')


class ResetPasswordForm(FlaskForm):
    """Form to reset the account password"""
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[
            DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset')


class ReviewForm(FlaskForm):
    """Form to input the different reviews about the application"""
    review = StringField(
        'Review', validators=[
            DataRequired(), Length(
                min=2, max=200)])
    name = StringField(
        'Name', validators=[
            DataRequired(), Length(
                min=2, max=200)])
    submit = SubmitField('Submit')


class EventForm(FlaskForm):
    """
    A form for scheduling an event with exercise selection, date, time, and friend invitation options.

    Fields:
        - exercise (SelectField): Dropdown to select an exercise from predefined choices.
          Choices include: Tennis, Badminton, Table Tennis, Yoga, Hiking, Jogging, Basketball, Dance.
        - date (DateField): Date selector for choosing the event date. Required field.
        - start_time (TimeField): Time field for specifying the start time of the event. Required field.
        - end_time (TimeField): Time field for specifying the end time of the event. Required field.
        - invited_friend (SelectField): Dropdown to select a friend to invite, with choices populated dynamically.
        - submit (SubmitField): Button to submit the form.

    Usage:
        - This form can be used in Flask templates to gather event scheduling details.
    """
    exercise_choices = [('Tennis', 'Tennis'), ('Badminton', 'Badminton'), ('Table Tennis', 'Table Tennis'), ('Yoga', 'Yoga'),
                        ('Hiking', 'Hiking'), ('Jogging', 'Jogging'), ('Basketball', 'Basketball'), ('Dance', 'Dance')]
    exercise = SelectField('Select an exercise', choices=exercise_choices)

    date = DateField('Select a Date', validators=[DataRequired()])

    start_time = TimeField('From', validators=[DataRequired()])

    end_time = TimeField('To', validators=[DataRequired()])

    invited_friend = SelectField('Invite a friend', choices=[])

    submit = SubmitField('Submit')
