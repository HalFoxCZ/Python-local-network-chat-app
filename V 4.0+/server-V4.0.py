import socket
from threading import Thread
from threadpool import ThreadPool as tPool

tPool = tPool(100)
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 42069
print(host)

while True:
    try:
        serversocket.bind((host, port))
        break
    except OSError:
        print("Port "+str(port)+" is already in use.")
        port += 1
        if port > 42099:
            print("No ports available.")
            exit(0)
print(serversocket.getsockname())
clientsockets = []
clientnames = []

def login(serversocket, addr, clientnames, clientsocket):
    while True:
        clients_online = ""
        for client in clientnames:
            clients_online += client + "\n"
        clientsocket.send(b"||SERVER||REQUEST_LOGIN||AND||SERVER||ONLINE_USER|?|"+clients_online)
        login = clientsocket.recv(1024)
        try:
            print(login.decode('ascii').split("|?|")[1])
            name = login.decode('ascii').split("|?|")[1]
            if name in clientnames:
                clientsocket.send(b"||SERVER||LOGIN||FAILED||")
            else:
                break
        except IndexError:
            print("Invalid login.")
    clientsockets.append(clientsocket)
    clientnames.append(name)
    print("Connection from: " + str(addr))
    tPool.add_task(clientsocket, name, clientsockets, task=dispatch_message)


def listener(serversocket, clientsocket, clientnames):
    while True:
        serversocket.listen()
        clientsocket, addr = serversocket.accept()
        tPool.add_task(serversocket, addr, clientnames, clientsocket, task=login)


def dispatch_message(skt, name, clientsockets):
    while True:
        try:
            msg = skt.recv(1024)
            msg = msg.decode('ascii')
            if  b"||CLIENT||LOGIN||RESPONSE|?|" in msg.encode('ascii'):
                print("connection attempt denied from:"+name)
                continue
            msg_send = name+": "+msg
            msg = "from:"+name+" - message: "+ msg
            print(msg)
            for skt_out in clientsockets:
                skt_out.send(msg_send.encode('ascii'))
        except:
            clientsockets.remove(skt)
            clientnames.remove(name)
            print("Connection closed.")
            break


tPool.add_task(serversocket, clientsockets, clientnames, task=listener)
