import socket
import threading

HOST = "localhost"
PORT = 6379

database = {}

def decode_resp(client):
    data = client.recv(1024)
    print(f"Received from client: {data}")
    
    delimiter = '\\r\\n'
    data = str(data).replace(delimiter, ' ').split(' ')
    
    command = ''
    arguments = []
    for i, string in enumerate(data):
        if '$3' in string:
            command = data[i + 1]
        elif '$4' in string:
            command = data[i + 1]
        elif '$5' in string:
            arguments.append(data[i + 1])
    return command, arguments


def handle_client(client):
    while True:
        try:
            command, arguments = decode_resp(client)
            if command == 'echo':
                message = bytes(f"${len(arguments[0])}\r\n{arguments[0]}\r\n", 'utf-8')
                client.send(message)
            elif command == 'get':
                k = arguments[0]
                message = bytes(f"${len(k)}\r\n{k}\r\n", 'utf-8')
                client.send(message)
            elif command == 'set':
                k, v = arguments
                database[k] = v                
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
