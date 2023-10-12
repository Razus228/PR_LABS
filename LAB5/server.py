
import socket 
import threading  
import json  
import os  
import base64  





HOST = '127.0.0.1'  
PORT = 12345  


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen()


chat_rooms = {}


# Function to handle client connections and messages
def client_handler(client_socket, client_address):
    print(f"New connection from {client_address}")  # Log new connection

    # Main loop to handle client messages
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        if not message:
            print(f"Connection closed by {client_address}")
            break
        message_json = json.loads(message)
        if message_json['type'] == 'connect':
            # Add client to the specified chat room
            room_name = message_json['payload']['room']
            user_name = message_json['payload']['name']
            if room_name not in chat_rooms:
                chat_rooms[room_name] = []
            chat_rooms[room_name].append((client_socket, user_name))
            # Send connection acknowledgment to client
            ack_message = {
                "type": "connect_ack",
                "payload": {
                    "message": "Connected to the room."
                }
            }
            client_socket.send(json.dumps(ack_message).encode('utf-8'))
            # Notify all clients in the room about the new connection
            notification_message = {
                "type": "notification",
                "payload": {
                    "message": f"{user_name} has joined the room."
                }
            }
            broadcast_message(room_name, notification_message, sender_socket=client_socket)
        elif message_json['type'] == 'message':
            # Broadcast text message to all clients in the room
            broadcast_message(message_json['payload']['room'], message_json, sender_socket=client_socket)
        elif message_json['type'] == 'file_upload':
            save_file(message_json['payload']['file_name'], message_json['payload']['file_data'])
            notification_message = {
                "type": "notification",
                "payload": {
                    "message": f"{message_json['payload']['file_name']} has been uploaded."
                }
            }
            try:
                broadcast_message(message_json['payload']['room'], notification_message,sender_socket=client_socket)
            except KeyError:
                print("Warning: The 'room' key was not found in the message payload.")
            # Additional error handling or logging code can go here if needed.
        elif message_json['type'] == 'file_download':
            send_file(client_socket, message_json['payload']['file_name'])

    # Remove client from chat rooms and close the socket
    for room_name, clients in chat_rooms.items():
        for client, user_name in clients:
            if client == client_socket:
                clients.remove((client, user_name))
                break
    client_socket.close()


# Function to broadcast message to all clients in a room
def broadcast_message(room_name, message_json, sender_socket=None):
    if room_name in chat_rooms:
        for client_socket, user_name in chat_rooms[room_name]:
            if client_socket != sender_socket:
                client_socket.send(json.dumps(message_json).encode('utf-8'))


# Function to save an uploaded file
def save_file(file_name, file_data):
    save_path = "Chat_TXT"  
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    file_path = os.path.join(save_path, file_name)
    decoded_file_data = base64.b64decode(file_data.encode('utf-8'))
    with open(file_path, "wb") as file:
        file.write(decoded_file_data)
    print(f"File saved at: {file_path}")


# Function to send a file to a client
def send_file(client_socket, file_name):
    file_path = os.path.join("Chat_TXT", file_name)
    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            file_data = file.read()
            encoded_file_data = base64.b64encode(file_data).decode('utf-8')
            file_message = {
                "type": "file",
                "payload": {
                    "file_name": file_name,
                    "file_data": encoded_file_data
                }
            }
            client_socket.send(json.dumps(file_message).encode('utf-8'))
            print(f"Sent file: {file_name}")
    else:
        notification_message = {
            "type": "notification",
            "payload": {
                "message": f"The file {file_name} does not exist."
            }
        }
        client_socket.send(json.dumps(notification_message).encode('utf-8'))
        print(f"File not found: {file_name}")


# Main loop to accept client connections
print("\nServer is running...\n")
print(f"Server is listening on {HOST}:{PORT}")
while True:
    client_socket, client_address = server_socket.accept()
    # Start a thread to handle the client
    client_thread = threading.Thread(target=client_handler, args=(client_socket, client_address))
    client_thread.start()