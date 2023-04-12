from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import message # import other models to create instances from here
from flask import flash # use flash to store validation messages

import re # import regex to validate email
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') # string to ensure valid email address
PASS_REGEX = re.compile(r'^(?!^[0-9]*$)(?!^[a-zA-Z]*$)^([a-zA-Z0-9!@#$%^&*()]{8,})$') # string to check password for letters and numbers

class User:
    DB = 'private_wall_schema'
    def __init__(self, data) -> None: # columns in database match instance attributes
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.num_messages = data['num_messages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.messages = [] # This list will store all of the messages the user has received

    # CRUD
    # CREATE
    @classmethod
    def add_user(cls, data):
        query = """INSERT INTO users (first_name, last_name, email, password)
                VALUES (%(fname)s, %(lname)s, %(email)s, %(password)s)"""
        return connectToMySQL(cls.DB).query_db(query, data) # returns row ID of new user
    # READ
    @classmethod
    def get_user_by_email(cls, data): # get db row from user email
        query = "SELECT * FROM users where email = %(email)s"
        results = connectToMySQL(cls.DB).query_db(query, data) # results in a list of one
        if len(results) < 1:
            return 0
        return cls(results[0]) # create an instance from db row and return it
    @classmethod
    def get_all_users(cls, data):
        query = "SELECT * FROM users WHERE NOT id = %(id)s ORDER BY first_name" # get every user except the one calling
        results = connectToMySQL(cls.DB).query_db(query, data) # put results into a list
        if not results: # if list is empty, return 0
            return 0
        all_users = []
        for db_row in results: # dictionary for this row to create instance of User
            row_user = {
                'id': db_row['id'],
                'first_name': db_row['first_name'],
                'last_name': db_row['last_name'],
                'email': db_row['email'],
                'password': db_row['password'],
                'num_messages': db_row['num_messages'],
                'created_at': db_row['created_at'],
                'updated_at': db_row['updated_at']
            }
            all_users.append(cls(row_user)) # add new instance to all_users list
        return all_users # return all_users list
    # UPDATE
    @classmethod
    def increase_message_counter(cls, data):
        query = "UPDATE users SET num_messages = num_messages + 1 WHERE id=%(id)s"
        return connectToMySQL(cls.DB).query_db(query, data)
    # static methods for user form validations
    @staticmethod
    def validate_registration(data):
        print('validating...')
        is_valid = True
        if len(data['fname']) < 2:
            flash('First name must have at least 2 characters.', 'registration')
            is_valid = False
        if len(data['lname']) < 2:
            flash('Last name must have at least 2 characters.', 'registration')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): 
            flash('Invalid email address!', 'registration')
            is_valid = False
        if User.get_user_by_email({'email': data['email']}):
            flash('Email is already in use.', 'registration')
            is_valid = False
        if not PASS_REGEX.match(data['password']):
            flash('Password must contain at least one letter, one number, and be at least 8 characters long.', 'registration')
            is_valid = False
        if data['confirm'] != data['password']:
            flash('Password does not match confirm password', 'registration')
            is_valid = False
        print('validation result:', is_valid)
        return is_valid