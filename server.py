from flask_app import app # import app to run controllers

# import controllers
from flask_app.controllers import users, messages

#import templates
from flask_app.templates import filters

if __name__ == '__main__':
    app.run(debug = True, port = 5001)