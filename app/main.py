import socket
import threading

HOST = "localhost"
PORT = 6379

def decode_resp(client):
    data = client.recv(1024)
    print(f"Received from client: {data}")
    
    delimiter = '\\r\\n'
    data = str(data).replace(delimiter, ' ').split(' ')
    
    command = b''
    argument = b''
    for i, string in enumerate(data):
        if '$4' in string:
            command = data[i + 1]
        elif '$5' in string:
            argument = bytes(data[i + 1], 'utf-8')
    return command, argument


def handle_client(client):
    while True:
        try:
            command, argument = decode_resp(client)            
            if 'echo' in command:
                message = bytes(f"${len(argument)}\r\n{argument}\r\n", 'utf-8')
                client.send(message)
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
