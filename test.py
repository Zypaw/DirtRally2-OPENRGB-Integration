import socket
DIRT_IP = ""  # Leave empty to listen on all interfaces
DIRT_PORT = 20777
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
sock.bind((DIRT_IP, DIRT_PORT))
while True:
    data, addr = sock.recvfrom(4096)  # Buffer size
    print("Received message:", data)
