import threading
import socket

host = '127.0.0.1'  # Local host
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()  # Method for server to listen to requests from clients

clients = []
usernames = []

def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            # Handle the case where sending the message fails
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast(f"{username} left the chat!".encode('ascii'))
            usernames.remove(username)

# Handling client connections
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            if message:
                broadcast(message)  # Broadcast message to all other clients
            else:
                # Handle the case where the client disconnects
                index = clients.index(client)
                clients.remove(client)
                client.close()
                username = usernames[index]
                broadcast(f"{username} left the chat!".encode('ascii'))
                usernames.remove(username)
                break
        except:
            # Handle any exceptions during message reception
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast(f"{username} left the chat!".encode('ascii'))
            usernames.remove(username)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")  # When a client connects

        client.send('NICK'.encode('ascii'))
        username = client.recv(1024).decode('ascii')
        usernames.append(username)
        clients.append(client)

        print(f'Username of the client is {username}!!')
        broadcast(f"{username} joined the chat".encode("ascii"))
        client.send("Connected to server!".encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is listening.....")
receive()