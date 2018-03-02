# Python program to implement client side of chat room.
import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP_address = '10.7.27.237'  # '10.7.24.67'#str(sys.argv[1])
Port = 5000  # int(sys.argv[2])
server.connect((IP_address, Port))

print('Please enter your ID:')
personname = input()
server.send(personname)

while True:

    # maintains a list of possible input streams
    sockets_list = [sys.stdin, server]

    """ There are two possible input situations. Either the
    user wants to give  manual input to send to other people,
    or the server is sending a message  to be printed on the
    screen. Select returns from sockets_list, the stream that
    is reader for input. So for example, if the server wants
    to send a message, then the if condition will hold true
    below.If the user wants to send a message, the else
    condition will evaluate as true"""
    read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])

    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048)
            if (len(message) != 0):
                print(message)
            else:
                sys.stdout.write("\nServer Down\n")
                sys.exit()
        else:
            message = sys.stdin.readline()
            server.send(str.encode(message))
            sys.stdout.write(personname)
            sys.stdout.write(message)
            sys.stdout.flush()
server.close()
