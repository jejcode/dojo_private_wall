from flask import Flask # import Flask to make an instance app
app = Flask(__name__) # create instance of Flask called app
app.secret_key = "I'll keep this key private. Shhhh."

