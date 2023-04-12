from flask_app import app # import app to run routes
from flask import render_template, redirect, session, request, flash # flask modules for routes to work
from flask_app.models import user,message # import models

@app.route('/send', methods=['POST'])
def send_message():
    if 'user_id' not in session:
        return redirect('/')
    # validate message
    if not message.Message.validate_message(request.form):
        return redirect('/wall')
    # send message by saving it in database
    data = {
        'message': request.form['message'],
        'sender_id': session['user_id'],
        'receiver_id': request.form['receiver_id']
    }
    message_id = message.Message.send_message(data)
    if message_id: # if message gets saved in database, up the count by one
        user.User.increase_message_counter({'id': session['user_id']})

    return redirect('/wall')

@app.route('/delete/<int:message_id>/<int:r_id>') #  route has validation for owner built in
def delete_message(message_id, r_id):
    if 'user_id' not in session:
        return redirect('/')
    if 'ip' in session:
        return redirect('/logout')
    # validate deletion by checking to see if user has the rights
    if session['user_id'] != r_id:
        session['ip'] = request.remote_addr
        return render_template('danger.html', message_id=message_id, ip=session['ip'])
    data = {
        'id': message_id,
    }
    result = message.Message.delete_message(data)
    return redirect('/wall')

@app.route('/delete/<int:id>') # this is a fake route. All traffic here is recorded for deletion
def fake_delete_message(id):
    if 'ip' in session:
        return redirect('/logout')
    # validate deletion by checking to see if user has the rights
    session['ip'] = request.remote_addr
    return render_template('danger.html', message_id=id, ip=session['ip'])

@app.route('/danger') # warning to page to stop being a delinquent
def issue_warning():
    return render_template('danger.html', ip = session['ip'])
