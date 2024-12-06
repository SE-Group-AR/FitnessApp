

"""
Copyright (c) 2024 Meet Patel, Anchita Ramani, Abhinav Jami
This code is licensed under MIT license (see LICENSE for details)

@author: ENERGIZE


This python file is used in and is part of the ENERGIZE project.

For more information about the ENERGIZE project, visit:
https://github.com/SE-Group-AR/FitnessApp

"""

"""Importing flask to connect to the database"""




from flask import Flask
from flask_pymongo import PyMongo
from flask_mail import Mail
class App:
    """Sending emails to friends"""

    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'secret'
        self.app.config['MONGO_URI'] = 'mongodb://localhost:27017/test'
        self.mongo = PyMongo(self.app)

        self.app.config['MAIL_SERVER'] = 'smtp.gmail.com'
        self.app.config['MAIL_PORT'] = 465
        self.app.config['MAIL_USE_SSL'] = True
        self.app.config['MAIL_USERNAME'] = "bogusdummy123@gmail.com"
        self.app.config['MAIL_PASSWORD'] = "helloworld123!"
        self.mail = Mail(self.app)
