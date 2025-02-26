import socket

# Client settings
HOST = 'localhost'
PORT = 11111

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((HOST, PORT))

while True:
    try:
        # Receive data from the server
        data = client_socket.recv(1024)
        if not data:
            break

        print(f"Received data: {data.decode()}")

    except Exception as e:
        print(f"Error occurred: {e}")
        break

# Close the connection
client_socket.close()
