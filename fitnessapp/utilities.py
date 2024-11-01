
"""
Copyright (c) 2024 Arkoh Lawrence, Lingjun Liu, Habib Mohammed
This code is licensed under MIT license (see LICENSE for details)

@author: ENERGIZE


This python file is used in and is part of the ENERGIZE project.

For more information about the ENERGIZE project, visit:
https://github.com/CSC510-GROUP-40/FitnessApp

"""
import random

from flask_mail import Message
from apps import App
import string


class Utilities:
    app = App()
    mail = app.mail
    mongo = app.mongo

    def send_email(self, email):
        msg = Message()
        msg.subject = "ENERGIZE - Reset Password Request"
        msg.sender = 'bogusdummy123@gmail.com'
        msg.recipients = [email]
        random = str(self.get_random_string(8))
        msg.body = 'Please use the following password to login to your account: ' + random
        self.mongo.db.ath.update({'email': email}, {'$set': {'temp': random}})
        if self.mail.send(msg):
            return "success"
        else:
            return "failed"

    def get_random_string(self, length):
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        print("Random string of length", length, "is:", result_str)
        return result_str
