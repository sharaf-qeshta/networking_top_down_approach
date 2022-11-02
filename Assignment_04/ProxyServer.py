from socket import *
import os

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(("localhost", 8000))
tcpSerSock.listen(1)
while 1:
    # Start receiving data from the client
    print('Ready to serve...')
    tcpCliSock, address = tcpSerSock.accept()
    message = tcpCliSock.recv(1024).decode()
    print("message: ", message)
    if message == '':
        continue
    # Extract the filename from the given message
    filename = message.split()[1].partition("/")[2]
    fileExist = False
    file_to_use = "/" + filename
    try:
        # Check whether the file exist in the cache
        f = open("WEB/" + file_to_use[1:], "rb")
        output_data = f.read()
        f.close()
        fileExist = True
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send("HTTP/1.1 200 OK\r\n".encode())
        tcpCliSock.send("Content-Type:text/html\r\n\r\n".encode())
        tcpCliSock.send(output_data)
        print('Read from cache')
    # Error handling for file not found in cache
    except IOError:
        if not fileExist:
            # Create a socket on the proxyServer
            c = socket(AF_INET, SOCK_STREAM)
            hostname = filename.replace("www.", "", 1)
            try:
                # Connect to the socket to port 80
                serverName = hostname.split("/")[0]
                c.connect((serverName, 80))
                askFile = ''.join(filename.partition('/')[1:])
                print(askFile)
                # Create a temporary file on this socket and ask port 80
                # for the file requested by the client
                file_obj = c.makefile('rwb', 0)
                file_obj.write(
                    "GET ".encode() + askFile.encode() + " HTTP/1.0\r\nHost: ".encode()
                    + serverName.encode() + "\r\n\r\n".encode())
                # Read the response into buffer
                serverResponse = file_obj.read()
                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket and the corresponding file in the cache
                filename = "WEB/" + filename
                file_split = filename.split('/')
                for i in range(0, len(file_split) - 1):
                    if not os.path.exists("/".join(file_split[0:i + 1])):
                        os.makedirs("/".join(file_split[0:i + 1]))
                tmpFile = open(filename, "wb")
                serverResponse = serverResponse.split(b'\r\n\r\n')[1]
                tmpFile.write(serverResponse)
                tmpFile.close()
                tcpCliSock.send("HTTP/1.1 200 OK\r\n".encode())
                tcpCliSock.send("Content-Type:text/html\r\n\r\n".encode())
                tcpCliSock.send(serverResponse)
            except:
                print("Illegal request")
            c.close()
        else:
            # HTTP response message for file not found
            tcpCliSock.send(f"HTTP/1.1 404 Not Found\n\n".encode())
    # Close the client and the server sockets
    tcpCliSock.close()
tcpSerSock.close()
