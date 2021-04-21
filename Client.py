import socket

HOST = '192.168.1.3'  # The server's hostname or IP address
PORT = 65432      # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    # s.send('Hello, world')
    filename='bsx1.jpg'
    f = open(filename,'rb')
    l = f.read(1024)
    while (l):
        s.send(l)
        # print('Sent ',repr(l))
        l = f.read(1024)
    f.close()
    print('Done sending')
    s.close()
