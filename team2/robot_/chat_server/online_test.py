from robot_chat_client import RobotChatClient
import serial
from flask import Flask
from flask_ask import Ask, statement
import time


ser = serial.Serial('/dev/ttyUSB0', 9600)
app = Flask(__name__)
ask = Ask(app, '/')

user_name = "unknown"
default_user = "jack"

group_status = {
    'jack' : 'offline',
    'Andrew' : 'offline',
    'Clovis' : 'offline',
}


check_status = None

@ask.intent("OnlineFriend",default = {'name': 'jack'})
def check_friend(name):
    global check_status
    check_status = None
    print(name);
    target = name;
    client_Yuchen.send({'sender': 'jack',
                 'type': 'command',
                 'target': name,
                 'command_name': 'is_online'});
    while check_status is None: 
        time.sleep(.02)

    if check_status == 'Yes':
        group_status[name] = 'online'
        speech_text = '{} is online, wanna have some funs...'.format(name)
    else:
        group_status[name] = 'offline'
        speech_text = '{} is not online, try to find someone else'.format(name)

    print(speech_text)
    return statement(speech_text).simple_card('Muscles', speech_text)


def test_callback(message_dict):
    global check_status
    print('Received dictionary {}'.format(message_dict))
    print('The message is type {}'.format(message_dict['type']))

    if message_dict['type'] == 'users':
        print('Number of users: {}'.format(message_dict['count']))
    elif message_dict['type'] == 'new_user':
        print('The new user is: {}'.format(message_dict['Username']))

    elif message_dict['type'] == 'command':
        if message_dict['target'] == default_user:
            print('Command target: {}\n'.format(message_dict['target']))
            print("The command is: " + message_dict['command_name'] + '\n')
            if message_dict['command_name'] == 'is_online':
                if(user_name == default_user):
                    message = 'Yes'
                else:
                    message = 'No'

            client_Yuchen.send({
                'type': 'Response',
                'sender': default_user,
                'message': message,
                'receiver': message_dict['sender']
                })

    elif message_dict['type'] == 'Response':
        if message_dict['receiver'] == default_user:
            check_status = message_dict['message']


if __name__ == '__main__':
    client_Yuchen = RobotChatClient('ws://ab5a6386ad26.ngrok.io', callback=test_callback)
    client_Yuchen.send({
             'type': 'new_user',
             'Username': 'jack',
             })
    app.run()