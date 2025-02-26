import socket
import threading

# Server settings
HOST = '0.0.0.0'
PORT = 11111

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(5)

print(f"Server listening on {HOST}:{PORT}")

# List to store client connections
clients = []


def handle_client(client_socket, address):
    print(f"New connection from {address}")
    clients.append(client_socket)

    while True:
        try:
            # Receive data from the client
            data = client_socket.recv(1024)
            if not data:
                break

            # Broadcast data to all clients except the sender
            for c in clients:
                if c != client_socket:
                    c.sendall(data)

            # Handle data from NiFi (if needed)
            print(f"Received data: {data.decode()}")

        except Exception as e:
            print(f"Error occurred: {e}")
            break

    # Remove client from the list and close the connection
    clients.remove(client_socket)
    client_socket.close()


while True:
    # Wait for a connection
    client_socket, address = server_socket.accept()

    # Create a new thread for the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
    client_thread.start()
