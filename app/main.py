import socket
import threading

HOST = "localhost"
PORT = 6379

def handle_client(client):
    while True:
        try:
            client.recv(1024)
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
