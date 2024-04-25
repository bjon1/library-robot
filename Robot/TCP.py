import socket
import time

class TCPServer:
    def __init__(self, host='137.140.181.67'):
        self.host = host
        self.port = 50000
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_server(self):
        # Bind the socket to a specific host and port
        self.server_socket.bind((self.host, self.port))

        # Enable the server to accept connections
        self.server_socket.listen()

        print(f'Server is listening on {self.host}:{self.port}')

        # Establish a connection with the client
        self.client_socket, addr = self.server_socket.accept()

        print(f'Got connection from {addr}')

        # Send a thank you message to the client
        self.client_socket.send(b'Thank you for connecting')

        while True:
            # Receive data from the client
            data = self.client_socket.recv(1024)
            
            uint8_data = [i for i in data]
        
            if len(uint8_data) <= 1:
                data = uint8_data[0]
            else:
                data = ''
                for i in uint8_data:
                    data += chr(i)

            print(f'Received data: {data}')
            time.sleep(0.05)
