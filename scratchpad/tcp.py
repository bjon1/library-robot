import socket
import time

def start_server(host='137.140.213.134', port=50000):
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific host and port
    server_socket.bind((host, port))

    # Enable the server to accept connections
    server_socket.listen()

    print(f'Server is listening on {host}:{port}')

    # Establish a connection with the client
    client_socket, addr = server_socket.accept()

    print(f'Got connection from {addr}')

    # Send a thank you message to the client
    client_socket.send(b'Thank you for connecting')

    while True:
        # Receive data from the client
        data = client_socket.recv(1024)
        
        uint8_data = [i for i in data]  # Convert bytes to list of integers
        if len(uint8_data) <= 1:
            data = uint8_data[0]
        else:
            data = ''
            for i in uint8_data:
                data += chr(i)

        print(f'Received data: {data}')
        time.sleep(0.05)

if __name__ == "__main__":
    start_server()