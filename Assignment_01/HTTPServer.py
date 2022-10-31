from socket import *


serverPort = 8000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("localhost", serverPort))
serverSocket.listen(1)
print("The server is ready to receive")

while True:
    connectionSocket, address = serverSocket.accept()
    request = connectionSocket.recv(1024).decode()
    requestData = request.split()
    fileName = requestData[1].replace("/", "")
    protocol = requestData[2]  # in case of HTTP/1.1 and HTTP/2
    try:
        file = open(fileName)
        data = file.read()
        connectionSocket.send(f"\n{protocol} 200 OK\n\n".encode())
        connectionSocket.send(data.encode())
    except IOError:
        connectionSocket.send(f"\n{protocol} 404 Not Found\n\n".encode())
    connectionSocket.close()
