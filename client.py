import socket
import threading
import argparse
from datetime import datetime , timedelta
import sys

#passcode check
parser = argparse.ArgumentParser(description='Server side code')
parser.add_argument('-join', action ='store_true')
parser.add_argument('-host', '--host', type=str, required=True)
parser.add_argument('-port','--port',type=int, required=True)
parser.add_argument('-username','--username',type=str,required=True)
parser.add_argument('-passcode','--passcode',type=str,required=True)
args = parser.parse_args()
passcode = args.passcode
userName = args.username

host = socket.gethostbyname(socket.gethostname())
port = args.port
hostName = args.host
format = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host,port))

def recieve_message():
    while True:
        try:
            message = client.recv(100).decode(format)
            if message == 'NAME':
                client.send(userName.encode(format))
            elif 'passcode:' in message:
                if passcode == message[9:]:
                    client.send('trueP'.encode(format))
                else:
                    print("Incorrect passcode")
                    sys.stdout.flush()
                    client.send('failP'.encode(format))
            elif 'Connected the server' == message:
                message = f'Connected to {hostName} on port {port}'
                print(message)
                sys.stdout.flush()
            else:
                print(message)
                sys.stdout.flush()
        except:
            print("ERROR")
            sys.stdout.flush()
            client.close()
            break
def write():
    while True:
        message = f'{userName}: {input("")}'
        if message[len(userName) + 2:] == ':)':
            message= f'{userName}: [feeling happy]'
        elif message[len(userName) + 2:] == ':(':
            message = f'{userName}: [feeling sad]'
        elif message[len(userName) + 2:] == ':mytime':
            currentTime = datetime.now()
            currentTime = currentTime.strftime('%a %B %d %H:%M:%S %Y')
            message= f'{userName}:{currentTime}'
        elif message[len(userName) + 2:] == ':+1hr':
            currentTime = datetime.now() + timedelta(hours=1)
            currentTime = currentTime.strftime('%a %B %d %H:%M:%S %Y')
            #currentTime = currentTime.strftime("%H:%M:%S")
            message= f'{userName}:{currentTime}'
        elif message[len(userName) + 2:] == ':Exit':
            print(f'{userName}: left the chatroom')
        client.send(message.encode(format))
recieve_thread = threading.Thread(target=recieve_message)
recieve_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
