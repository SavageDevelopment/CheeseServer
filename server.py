import threading
import socket
import time

host = '0.0.0.0'
port = 59872

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
names = []

def broadcast(message):
    for client in clients:
        client.send(message)



def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            name = names[index]
            broadcast(f'{name} left the game!'.encode('ascii'))
            names.remove(name)
            break

def admincmds():
    while True:
        command = input()
        if command == '/sq':
            broadcast('SAVSQ'.encode('ascii'))
            time.sleep(3)
            broadcast('[SERVER] Welcome to the Cheese Quiz!'.encode('ascii'))
            time.sleep(1)
            broadcast('Question 1'.encode('ascii'))
            time.sleep(1)
            broadcast('INSERT QUESTION'.encode('ascii'))
            broadcast('SAVO'.encode('ascii'))

        

def recieve():
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        client.send('NAME'.encode('ascii'))
        name = client.recv(1024).decode('ascii')
        names.append(name)
        clients.append(client)

        print(f'Name of Client is {name}')
        broadcast(f'{name} joined the game!'.encode('ascii'))
        client.send('Connected to the Game!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

admincmds_thread = threading.Thread(target=admincmds)
admincmds_thread.start()

print('Server is on...')
recieve()
