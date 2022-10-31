from socket import *
import time

'''
Round Trip Time (RTT) for packet 1 is 1996 Microseconds
Round Trip Time (RTT) for packet 2 is 0 Microseconds
Round Trip Time (RTT) for packet 3 is 0 Microseconds
Round Trip Time (RTT) for packet 4 is 996 Microseconds
Round Trip Time (RTT) for packet 5 is 0 Microseconds
Round Trip Time (RTT) for packet 6 is 0 Microseconds
Round Trip Time (RTT) for packet 7 is 0 Microseconds
Round Trip Time (RTT) for packet 8 is 0 Microseconds
Round Trip Time (RTT) for packet 9 is 0 Microseconds
Round Trip Time (RTT) for packet 10 is 997 Microseconds
'''

serverName = "localhost"
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)

for i in range(1, 11):
    try:
        message = f"Message{i}"
        start = int(time.time() * 1000000)
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        end = int(time.time() * 1000000)
        print(f"Round Trip Time (RTT) for packet {i} is {end - start} Microseconds")
    except Exception:
        print(f"packet {i} lost")

clientSocket.close()
