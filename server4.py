# Python program to implement server side of chat room.
import socket
import select
import sys
from _thread import *
import random
import pickle, pprint

"""The first argument AF_INET is the address domain of the
socket. This is used when we have an Internet Domain with
any two hosts The second argument is the type of socket.
SOCK_STREAM means that data or characters are read in
a continuous flow."""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


# IP_address = '10.7.28.116'   # '10.7.24.67'#str(sys.argv[1])
IP_address = 'REPLACETHIS'

# takes second argument from command prompt as port number
# Port = 5432

Port = 5432

"""
binds the server to an entered IP address and at the
specified port number.
The client must be aware of these parameters
"""
server.bind((IP_address, Port))
Porttosend = server.getsockname()

"""
listens for 100 active connections. This number can be
increased as per convenience.
"""
server.listen(100)

list_of_clients = []

messages = []




def write_to_file(data, filename):
    output = open(filename, 'wb')
    pickle.dump(data, output)
    output.close()

def read_file(filename):
    with open(filename, 'rb') as f:
        content = pickle.load(f)
    return messages

write_to_file(messages, 'data.pkl')

def clientthread(conn, addr, userID):

    # sends a message to the client whose user object is conn
    conn.send("Welcome to this chatroom!".encode("UTF-8"))

    while True:
            try:
                message = conn.recv(2048)
                
                if True:

                    """prints the message and address of the
                    user who just sent the message on the server
                    terminal"""
                    print('<', userID.decode('UTF-8'), '>', message.decode('UTF-8'))

                    # Calls broadcast function to send message to all
                    message_to_send = "<" + userID.decode('UTF-8') + "> " + message.decode('UTF-8')

                    messages.append(message_to_send)
                    write_to_file(messages, 'data.pkl')

                    broadcast(message_to_send.encode('UTF-8'), conn)

                else:
                    """message may have no content if the connection
                    is broken, in this case we remove the connection"""
                    remove(conn)

            except:
                continue


"""Using the below function, we broadcast the message to all
clients who's object is not the same as the one sending
the message """


def broadcast(message, connection):
    for clients in list_of_clients:
        if clients != connection:
            try:
                clients.send(message)
            except:
                clients.close()

                # if the link is broken, we remove the client
                remove(clients)


"""The following function simply removes the object
from the list that was created at the beginning of
the program"""


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


while True:

    """Accepts a connection request and stores two parameters,
    conn which is a socket object for that user, and addr
    which contains the IP address of the client that just
    connected"""
    conn, addr = server.accept()
    userID = conn.recv(2048)
    # print(userID)
    # print(type(userID) is str)

    """Maintains a list of clients for ease of broadcasting
    a message to all available people in the chatroom"""
    list_of_clients.append(conn)

    # prints the address of the user that just connected
    print(userID.decode('UTF-8'), " connected")

    # creates and individual thread for every user
    # that connects
    start_new_thread(clientthread, (conn, addr, userID))

conn.close()
server.close()
