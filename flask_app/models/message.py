from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user # import other models to create instances from here
from flask import flash # use flash to store validation messages
class Message:
    DB = 'private_wall_schema'
    def __init__(self, data) -> None: # columns in database match instance attributes
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.sender = None # will be instance of user
        self.receiver = None # will be instance of recipient of message

    # CRUD
    #CREATE
    @classmethod
    def send_message(cls, data):
        query = """INSERT INTO messages (content, sender_id, receiver_id)
                VALUES (%(message)s, %(sender_id)s, %(receiver_id)s)"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    # READ
    @classmethod
    def get_message_data(cls, data): # query gets all messages for requesting user
        query = """SELECT * FROM users
                LEFT JOIN messages ON users.id = receiver_id
                LEFT JOIN users AS senders ON sender_id = senders.id
                WHERE users.id = %(id)s"""
        results = connectToMySQL(cls.DB).query_db(query, data) # results in list of db rows
        if not results:
            return 0
        all_user_messages = []
        for db_row in results:
            this_row_message = { # dictionary to create Message instance
                'id': db_row['messages.id'],
                'content': db_row['content'],
                'created_at': db_row['messages.created_at'],
                'updated_at': db_row['messages.updated_at'],
            }
            this_message = cls(this_row_message) # create instance of Message
            this_row_sender = {
                'id': db_row['senders.id'],
                'first_name': db_row['senders.first_name'],
                'last_name': db_row['senders.last_name'],
                'email': db_row['senders.email'],
                'password': db_row['senders.password'],
                'num_messages': db_row['senders.num_messages'],
                'created_at': db_row['senders.created_at'],
                'updated_at': db_row['senders.updated_at']
            }
            this_message.sender = user.User(this_row_sender) # link instance to sender
            this_row_receiver = {
                'id': db_row['id'],
                'first_name': db_row['first_name'],
                'last_name': db_row['last_name'],
                'email': db_row['email'],
                'password': db_row['password'],
                'num_messages': db_row['num_messages'],
                'created_at': db_row['created_at'],
                'updated_at': db_row['updated_at']
            }
            this_message.receiver = user.User(this_row_receiver) # link instance to receiver
            all_user_messages.append(this_message)
        return all_user_messages
    # DELETE
    @classmethod
    def delete_message(cls, data): # delete message from database
        query = "DELETE FROM messages WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query, data)
    @staticmethod
    def validate_message(data):
        is_valid = True
        if len(data['message']) < 5:
            flash('Messages must be have at least 5 characters.', 'send_attempt')
            is_valid = False
        return is_valid

