import socket
import threading
import time

HOST = "localhost"
PORT = 6379

database = {}
expires = {}

def decode_resp(client):
    data = client.recv(1024)
    delimiter = '\\r\\n'
    data = str(data).replace(delimiter, ' ')
    print(f"Received from client: {data}")
    data = data.split(' ')
    
    command = ''
    arguments = []
    for i, string in enumerate(data):
        if string in ['echo', 'set', 'get']:
            command = string
        elif string in ['$5', '$9']:
            arguments.append(data[i + 1])
        elif string == 'px':
            arguments.append(int(data[i + 2]))
    return command, arguments


def handle_client(client):
    while True:
        try:
            command, arguments = decode_resp(client)
            print(command, arguments)
            if command == 'echo':
                message = bytes(f"${len(arguments[0])}\r\n{arguments[0]}\r\n", 'utf-8')
                client.send(message)
                
            elif command == 'get':
                k = arguments[0]
                
                if expires.get(k) is None:
                    message = bytes(f"${len(k)}\r\n{database[k]}\r\n", 'utf-8')
                else:
                    if time.time() > expires.get(k):
                        message = "$-1\r\n".encode()
                    else:
                        message = bytes(f"${len(k)}\r\n{database[k]}\r\n", 'utf-8')
                client.send(message)
                
            elif command == 'set':                
                k, v = arguments[:2]
                database[k] = v
                
                if len(arguments) == 3:
                    px = arguments[-1]
                    expires[k] = time.time() + (px / 1000.0)          
                client.send(b"+OK\r\n")
                
            else:
                client.send(b"+PONG\r\n")
        except ConnectionError:
            break

def main():
    with socket.create_server((HOST, PORT), reuse_port=True) as server:
        while True:
            client, addr = server.accept() # wait for client
            print(f"Connected by {addr}")
            threading.Thread(target=handle_client, args=(client,)).start()

if __name__ == "__main__":
    main()
