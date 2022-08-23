import threading
import socket
import argparse
from datetime import datetime , timedelta
import sys

host = socket.gethostbyname(socket.gethostname())
format = 'utf-8'

parser = argparse.ArgumentParser(description='Server side code')
parser.add_argument('-start', action ='store_true')
parser.add_argument('-port','--port',type=int, required=True)
parser.add_argument('-passcode','--passcode',type=str,required=True)

args = parser.parse_args()

passcode = args.passcode
port = args.port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

clients = []
userName_list = []

def broadcast(message, nickname , nicknames):
    i = 0
    for client in clients:
        if nickname != nicknames[i]:
            client.send(message)
            i=i+1

def multi_user_handler(client):
    while True:
        try:
            message = client.recv(100)
            if ' :Exit'.encode(format) in message:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = userName_list[index]
                print(f'{nickname} left the chatroom')
                sys.stdout.flush()
                broadcast(f'{nickname} left the chatroom'.encode(format),None,userName_list)
                userName_list.remove(nickname)
                break
            if 'failP'.encode(format) in message:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = userName_list[index]
                broadcast(f'{nickname} enter wrong passwrod'.encode(format),None,userName_list)
                userName_list.remove(nickname)
                break
            else:
                print(message.decode(format))
                sys.stdout.flush()
                broadcast(message,None,userName_list)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = userName_list[index]
            broadcast(f'{nickname} left the chat'.encode(format),None,userName_list)
            userName_list.remove(nickname)
            break
def recieve_message():
    while True:
        client, address = server.accept()
        #check the name
        client.send('NAME'.encode(format))
        currentUserName = client.recv(100).decode(format)
        #check the passcode
        client.send(f'passcode:{passcode}'.encode(format))
        passcodeCheck = client.recv(100).decode(format)
        userName_list.append(currentUserName)
        clients.append(client)

        if passcodeCheck == 'trueP':
            print(f'{currentUserName} joined the chatroom')
            sys.stdout.flush()
            broadcast(f'{currentUserName} joined the chatroom'.encode(format),currentUserName,userName_list)
            client.send('Connected the server'.encode(format))
            thread = threading.Thread(target=multi_user_handler, args= (client,))
            thread.start()
        elif passcodeCheck == 'failP':
            index = clients.index(client)
            clients.remove(client)
            client.close()
            currentUserName = userName_list[index]
            broadcast(f'{currentUserName} enter wrong password'.encode(format),currentUserName,userName_list)
            userName_list.remove(currentUserName)
print(f'Server started on port {port}. Accepting connections')
sys.stdout.flush()
recieve_message()





