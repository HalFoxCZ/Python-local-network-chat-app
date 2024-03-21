import socket
from threading import Thread
from threadpool import ThreadPool as tPool

tPool = tPool(50)

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
port = 42069

print(host)

serversocket.bind((host, port))
print(serversocket.getsockname())

clientsockets = [

]

def listener(serversocket, clientsocket):
    while True:
        serversocket.listen()
        clientsocket, addr = serversocket.accept()
        clientsockets.append(clientsocket)
        print("Connection from: " + str(addr))
        tPool.add_task(clientsocket, clientsockets, task=dispatch_message)

def dispatch_message(skt, clientsockets):

    while True:
        try:
            msg = skt.recv(1024)
            print("from:"+skt.getpeername()[0]+" - message: "+ msg.decode('ascii'))
            for skt_out in clientsockets:
                skt_out.send(msg)
        except ConnectionResetError:
            print("Connection closed.")
            break

tPool.add_task(serversocket, clientsockets, task=listener)
