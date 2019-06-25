#!/usr/bin/env python3.4
'''
The Chat Client
'''
import select
import socket
import sys
from connectdb import connection
import tkinter


def get_or_create(username):
    '''
    If username exists, log in else register user
    '''
    uname = None
    try:
        with connection.cursor() as cursor:
            # look for username
            sql = "SELECT * FROM users WHERE username=%s"
            cursor.execute(sql, username)
            result = cursor.fetchone()            
            if result:
                uname = result['username']
            else:
                raise
    except:
        with connection.cursor() as cursor:
            sql = "INSERT INTO users (username) VALUES (%s)"
            cursor.execute(sql, username)
        connection.commit()
        uname = username
    finally:
        connection.close()
    return uname


def get_users():
    '''
    Return all users
    '''
    try:
        with connection.cursor() as cursor:
            sql = "SELECT username FROM users"
            cursor.execute(sql)
            result = cursor.fetchall()            
            if len(result) > 0:
                for res in result:
                    print(res['username'])
    except:
        print('Something weird. Try again')


def users_messages(user, num):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT message, sender FROM messages WHERE username = %s LIMIT %s"
            cursor.execute(sql, (user, num))
            result = cursor.fetchall()            
            if len(result) > 0:
                for i, res in enumerate(result):
                    i += 1
                    print('{}: {} said {}'.format(
                        i, res['sender'], res['message']))
            else:
                print('Empty results')
    except:
        print('User not found. Try again')


def prompt():    
    sys.stdout.write('You > ')
    sys.stdout.flush()


class ChatClient:

    def __init__(self, host, port, username):
        self.username = get_or_create(username)
        self.host = host
        self.port = port
        self.csocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tkinter.mainloop()  # Starts GUI execution.

        # connect to remote host
        try:
            self.csocket.connect((self.host, self.port))
        except:
            print('Unable to connect')

            sys.exit()

        print('You are Connected. username: message \n Please C^out to quit')
        self.csocket.send(bytes(username, 'utf-8'))
        prompt()

    def run(self):
        while True:
            socket_list = [sys.stdin, self.csocket]

            # Get the list sockets which are readable
            read_sockets, write_sockets, error_sockets = select.select(
                socket_list, [], [])

            for sock in read_sockets:
                # incoming message from remote server
                if sock == self.csocket:
                    data = sock.recv(1024)
                    if not data:
                        print('\nDisconnected from chat server')
                        sys.exit()
                    else:
                        # print data
                        print("\r", data.decode('utf-8'), end="")
                        prompt()

                # user entered a message
                else:
                	msg = my_msg.get()
                	my_msg.set("")  # Clears input field
                	msg = sys.stdin.readline()
                	if msg:
                		self.csocket.send(bytes(msg, 'utf-8'))
                	else:
                		print('The Format must be username: message ')
                	prompt()
            
top = tkinter.Tk()
top.title("LANCAS")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=25, width=100, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", prompt)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=prompt)
send_button.pack()

# top.protocol("WM_DELETE_WINDOW", on_closing)


if __name__ == '__main__':

    if(len(sys.argv) == 2):
        if sys.argv[1] == 'users':
            get_users()
        else:
            print('Usage : ./client.py users')
            sys.exit()

    elif(len(sys.argv) == 3):
        user = sys.argv[1]
        num = int(sys.argv[2])

        if num < 0:
            print('Number of messages show be a positive integer')
            print('Usage : ./client.py username 10')
            sys.exit()
        users_messages(user, num)

    else:
        name = input('Welcome! Enter your username > ')
        cchat = ChatClient('127.0.0.1', 5700, name)
        cchat.run()
        
