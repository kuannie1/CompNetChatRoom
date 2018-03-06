# Python program to implement client side of chat room.
import socket
import select
import sys


def chat_client():

    # IP_address = sys.argv[1]
    # Port = int(sys.argv[2])

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Please enter your ID:')
    personname = input()

    IP_address = '127.0.0.1'  # '10.7.24.67'#str(sys.argv[1])
    Port = 5432  # int(sys.argv[2
    try:
        server.connect((IP_address, Port))

    except:
        print('Unable to connect')
        sys.exit()

    server.send(personname.encode('UTF-8'))
    print('Connected to server as ' + personname + '! Start writing your msg')
    sys.stdout.flush()

    while True:

            # maintains a list of possible input streams
        sockets_list = [sys.stdin, server]
        """ There are two possible input situations. Either the
        user wants to give  manual input to send to
         other people,
        or the server is sending a message  to be printed on the
        screen. Select returns from sockets_list, the stream that
        is reader for input. So for example, if the server wants
        to send a message, then the if condition will hold true
        below.If the user wants to send a message, the else
        condition will evaluate as true"""
        read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])
        for socks in read_sockets:
            if socks == server:
                # incoming message from the server
                message = socks.recv(2048)
                if (len(message) != 0):
                    print(message.decode('UTF-8'))
                else:
                    # there's no connection
                    sys.stdout.write("Server Down")
                    sys.exit()
            else:
                # user entered a message
                message = sys.stdin.readline()
                server.send(message.encode('UTF-8'))
                personname2 = '< ' + personname + ' > '
                sys.stdout.write(personname2+message)
                # sys.stdout.write(message)
                sys.stdout.flush()
    server.close()


if __name__ == "__main__":
    sys.exit(chat_client())
