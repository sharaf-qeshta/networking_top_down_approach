from socket import *

'''
sample run
b"220 ('127.0.0.1', 60989)"
b'250 Hello Localhost\r\n, pleased to meet you'
b'250 SharafQeshta@example.edu\r\n ... Sender ok'
b'250 JohnSmith@example.org \r\n ... Recipient ok'
b'354 Enter mail, end with "." on a line by itself'
b'250 Message accepted for delivery'
'''
mail_server = "localhost"
mail_port = 25

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((mail_server, mail_port))

ready_code = client_socket.recv(1024)
print(ready_code)
if ready_code.split()[0] != b'220':
    print("Error occurs")

client_socket.send("Hello Localhost\r\n".encode())
response_1 = client_socket.recv(1024)
print(response_1)
if response_1.split()[0] != b'250':
    print("Error occurs")


client_socket.send("MAIL FROM: <SharafQeshta@example.edu>\r\n".encode())
response_2 = client_socket.recv(1024)
print(response_2)
if response_2.split()[0] != b'250':
    print("Error occurs")


client_socket.send("RCPT TO: <JohnSmith@example.org> \r\n".encode())
response_3 = client_socket.recv(1024)
print(response_3)
if response_3.split()[0] != b'250':
    print("Error occurs")


client_socket.send("DATA\r\n".encode())
response_4 = client_socket.recv(1024)
print(response_4)
if response_4.split()[0] != b'354':
    print("Error occurs")

client_socket.send("Hello World\r\n".encode())
client_socket.send("\n\r.\r\n".encode())
response_5 = client_socket.recv(1024)
print(response_5)
if response_5.split()[0] != b'250':
    print("Error occurs")

client_socket.send("QUIT\r\n".encode())
client_socket.close()