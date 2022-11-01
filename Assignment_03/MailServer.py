from socket import *

'''
sample run =>
The server is ready to receive
"From": SharafQeshta@example.edu
"To": JohnSmith@example.org 
"Subject": Hello World
Hello World1
Hello World2
.
'''
serverPort = 25
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("localhost", serverPort))
serverSocket.listen(1)
print("The server is ready to receive")

while True:
    mail = "\"From\": ?\"To\": !\"Subject\": `"
    connectionSocket, address = serverSocket.accept()
    connectionSocket.send(f"220 {address}".encode())

    hello = connectionSocket.recv(1024).decode()
    connectionSocket.send(f"250 {hello}, pleased to meet you".encode())

    mail_from = connectionSocket.recv(1024).decode()
    sender = mail_from.split("<")[1].replace(">", "")
    mail = mail.replace("?", sender)
    connectionSocket.send(f"250 {sender} ... Sender ok".encode())

    mail_to = connectionSocket.recv(1024).decode()
    recipient = mail_to.split("<")[1].replace(">", "")
    mail = mail.replace("!", recipient)
    connectionSocket.send(f"250 {recipient} ... Recipient ok".encode())

    connectionSocket.recv(1024)  # DATA
    connectionSocket.send("354 Enter mail, end with \".\" on a line by itself".encode())

    subject = connectionSocket.recv(1024).decode()
    while not subject.strip().endswith("."):
        subject = f"{subject}\n{connectionSocket.recv(1024).decode()}"
    mail = mail.replace("`", subject.strip())

    connectionSocket.send("250 Message accepted for delivery".encode())
    connectionSocket.recv(1024)  # QUIT
    connectionSocket.send(f"221 {address} closing connection".encode())
    connectionSocket.close()
    print(mail)
