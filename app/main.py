import socket


def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    client, _ = server_socket.accept() # wait for client
    _ = client.recv(4096)
    client.send(b"+PONG\r\n")

if __name__ == "__main__":
    main()
