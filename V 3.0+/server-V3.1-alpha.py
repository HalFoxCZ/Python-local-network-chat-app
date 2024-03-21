import socket
from threading import Thread
from threadpool import ThreadPool as tPool
import tkinter as tk

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

root = tk.Tk()
root.title("[SERVER] : chat-app")
root.geometry("500x600")

clients_name = tk.StringVar()
clients_name.set("Users:")

clients = tk.Label(
    root,
    textvariable=clients_name
)

socket_info = tk.StringVar()
socekt_text = ""
sockets = serversocket.getsockname()
for socket in sockets:
    socekt_text += str(socket)
socket_info.set("Server socket info: "+socekt_text)

socket_info_label = tk.Label(
    root,
    textvariable=socket_info
)

logging = tk.StringVar()
logging.set("")

logging_label = tk.Label(
    root,
    textvariable=logging
)

logging_text = tk.StringVar()
logging_text.set("Logging:")

logging_text_label = tk.Label(
    root,
    textvariable=logging_text
)

logging_text_label.grid(row=2, column=1, columnspan=10)
logging_label.grid(row=3, column=1, columnspan=10)
clients.grid(row=1, column=1, columnspan=10)
socket_info_label.grid(row=0, column=1, columnspan=10)

def login(serversocket, addr, clientnames, clientsocket, clients_name, logging):
    while True:
        for client in clientnames:
            clientsocket.send(b"||SERVER||ONLINE_USER|?|"+client.encode('ascii'))
        clientsocket.send(b"||SERVER||REQUEST_LOGIN||")
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
    clients_name.set(clients_name.get()+"\n"+name+" : "+str(addr))
    logging.set(logging.get()+"\n"+"Connection from: `"+str(addr)+"`, name: `"+name+"`")
    clientsockets.append(clientsocket)
    clientnames.append(name)
    print("Connection from: " + str(addr))
    tPool.add_task(clientsocket, name, clientsockets, logging, clients_name, task=dispatch_message)


def listener(serversocket, clientsocket, clientnames, logging, clients_name):
    while True:
        serversocket.listen()
        clientsocket, addr = serversocket.accept()
        tPool.add_task(serversocket, addr, clientnames, clientsocket, clients_name, logging, task=login)


def dispatch_message(skt, name, clientsockets, logging, clients_name):
    while True:
        try:
            msg = skt.recv(1024)
            msg = msg.decode('ascii')
            if msg == "":
                clientNamesLocal = clients_name.get().split("\n")
                clients_new = ""
                for client in clientNamesLocal:
                    if not name in client:
                        clients_new += client
                clients_name.set(clients_new)
                clientsockets.remove(skt)
                clientnames.remove(name)
                print("Connection closed.")
                break
            if  b"||CLIENT||LOGIN||RESPONSE|?|" in msg.encode('ascii'):
                print("conetion attemtp denied from:"+name)
                continue
            msg_send = name+": "+msg
            msg = "from:"+name+" - message: "+ msg
            logging.set(logging.get()+"\n"+msg)
            print(msg)
            for skt_out in clientsockets:
                skt_out.send(msg_send.encode('ascii'))
        except:
            clientNamesLocal = clients_name.get().split("\n")
            clients_new = ""
            for client in clientNamesLocal:
                if not name in client:
                    clients_new += client
            clients_name.set(clients_new)
            clientsockets.remove(skt)
            clientnames.remove(name)
            print("Connection closed: "+name)
            break


tPool.add_task(serversocket, clientsockets, clientnames, logging, clients_name, task=listener)
root.mainloop()
