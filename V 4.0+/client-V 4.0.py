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
        print("Port " + str(port) + " is already in use.")
        port += 1
        if port > 42099:
            print("No ports available.")
            exit(0)

print(serversocket.getsockname())
clientsockets = []
clientnames = []

tk_socket_info = serversocket.getsockname()

tk_socket_info_string = ""
tk_socket_info_string += "SERVER SOCKET INFO: "

for i in range(len(tk_socket_info)):
    tk_socket_info_string += str(tk_socket_info[i]) + " "

root = tk.Tk()
root.title("[SERVER] - Chat app")
root.geometry("500x600")

tk_server_socket_info = tk.StringVar()
tk_server_socket_info.set(tk_socket_info_string)

tk_server_socket_info_label = tk.Label(
    root,
    textvariable=tk_server_socket_info
)

tk_online_user_text = tk.StringVar()
tk_online_user_text.set("USERS ONLINE:")

tk_online_user_label = tk.Label(
    root,
    textvariable=tk_online_user_text
)

tk_server_logging_text = tk.StringVar()
tk_server_logging_text.set("SERVER LOGGING: ")

tk_server_logging_text_label = tk.Label(
    root,
    textvariable=tk_server_logging_text
)

tk_server_logging = tk.StringVar()
tk_server_logging.set("")

tk_server_logging_label = tk.Label(
    root,
    textvariable=tk_server_logging
)
tk_server_socket_info_label.grid(row=0, column=0, columnspan=2)
tk_online_user_label.grid(row=1, column=0, columnspan=2)

tk_server_logging_text_label.grid(row=2, column=0, columnspan=2)
tk_server_logging_label.grid(row=3, column=0, columnspan=2)

root.mainloop()


def login(addr, clientnames, clientsocket, logging, tk_user_list):
    while True:
        clients_online = ""
        for client in clientnames:
            clients_online += client + "\n"

        clientsocket.send(b"||SERVER||REQUEST_LOGIN||AND||SERVER||ONLINE_USER|?|" + clients_online)
        login = clientsocket.recv(1024)
        try:
            print(login.decode('ascii').split("|?|")[1])
            name = login.decode('ascii').split("|?|")[1]
            if name in clientnames:
                clientsocket.send(b"||SERVER||LOGIN||FAILED||")
                logging.set(logging.get() + "\n" + "connection attempt denied from:" + addr)
            else:
                break
        except IndexError:
            print("Invalid login.")

    clientsockets.append(clientsocket)
    clientnames.append(name)
    print("Connection from: " + str(addr))
    loggin.set(logging.get() + "\n" + name + " have connected.")
    tPool.add_task(clientsocket, name, clientsockets, task=dispatch_message)


def listener(serversocket, clientsocket, clientnames, logging, tk_user_list):
    while True:
        serversocket.listen()
        clientsocket, addr = serversocket.accept()
        tPool.add_task(addr, clientnames, clientsocket, logging, tk_user_list, task=login)


def dispatch_message(skt, name, clientsockets, logging, tk_user_list):
    while True:
        try:
            msg = skt.recv(1024)
            msg = msg.decode('ascii')
            if b"||CLIENT||LOGIN||RESPONSE|?|" in msg.encode('ascii'):
                print("connection attempt denied from:" + name)
                logging.set(logging.get() + "\n" + "connection attempt denied from:" + name)
                continue
            msg_send = name + ": " + msg
            msg = "from:" + name + " - message: " + msg
            logging.set(logging.get() + "\n" + msg)
            print(msg)
            for skt_out in clientsockets:
                skt_out.send(msg_send.encode('ascii'))
        except:
            clientsockets.remove(skt)
            clientnames.remove(name)
            list_new = "USERS ONLINE: \n"
            for client in tk_user_list:
                if name in client:
                    continue
                else:
                    list_new += client + "\n"
            print("Connection closed from: " + name)
            logging.set(logging.get() + "\n" + name + " have disconnected.")
            break


tPool.add_task(serversocket, clientsockets, clientnames, tk_server_logging_label, tk_online_user_label, task=listener)
