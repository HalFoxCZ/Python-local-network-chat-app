import socket
from threading import Thread
from threadpool import ThreadPool as tPool
import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime


def getTime():
    return datetime.now().strftime("%H:%M:%S")

print(getTime())

tPool = tPool(100)
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 42069
print(host)

while True:
    try:
        serversocket.bind((host, port))
        break
    except:
        print("Port "+str(port)+" is already in use.")
        port += 1
        if port > 42099:
            print("No ports available.")
            exit(0)
print(serversocket.getsockname())
clientsockets = []
clientnames = []

 # ======================================= TKINTER SETTUP =======================================


root = tk.Tk()
root.title("[SERVER] : chat-app")

ttk.Style(root).theme_use("vista")
print(ttk.Style(root).theme_use())
print(ttk.Style(root).theme_names())
w = 1024 # width for the Tk root
h = 750 # height for the Tk root

# get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen

root.configure(background="#222")
# calculate x and y coordinates for the Tk root window
x = 0
y = 0

# set the dimensions of the screen
# and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

clients_name = tk.StringVar()
clients_name.set("Users:")
clients = tk.Label(
    root,
    textvariable=clients_name,
    anchor="nw",
    justify="left",
    width= 1024,
    height=15,
    background="#222",
    foreground="white",
    font=('Comic Sans MS', 12, 'bold italic'),

)

s = ttk.Style()
s.theme_names()
s.theme_use("clam")
s.theme_use("vista")

socket_info = tk.StringVar()
socket_info.set("Server socket info: "+str(serversocket.getsockname()))

socket_info_label = tk.Label(
    root,
    textvariable=socket_info,
    anchor="nw",
    justify="left",
    width= 1024,
    background="#222",
    foreground="white",
    font=('Comic Sans MS', 12, 'bold italic'),

)

logging = tk.StringVar()
logging.set("")


logging_text = tk.StringVar()
logging_text.set("Logging:")
logging_text_label = tk.Label(
    root,
    textvariable=logging_text,
    anchor="nw",
    justify="left",
    width= 1024,
    background="#222",
    foreground="white",
    font=('Comic Sans MS', 12, 'bold italic'),

)

close_button = tk.Button(
    root,
    text="Close server",
    command=lambda: closeServer(serversocket),
    background="#222",
    foreground="white",
    height=2,
    width=15,
    font=('Comic Sans MS', 12, 'bold italic')
)


logging_label = tk.Label(
    root,
    textvariable=logging,
    anchor="nw",
    justify="left",
    width=1024,
    background="#222",
    foreground="white",
    font=('Comic Sans MS', 12, 'bold italic'),
    height=root.winfo_height()-(logging_text_label.winfo_height()+clients.winfo_height()+socket_info_label.winfo_height()+close_button.winfo_height())
)

socket_info_label.grid(row=0, column=0, )
clients.grid(row=1, column=0,)
close_button.grid(row=2, column=0 )
logging_text_label.grid(row=3, column=0, )
logging_label.grid(row=4, column=0, )



# ======================================= FUNCTIONS SETTUP =======================================
def login(serversocket, addr, clientnames, clientsocket, root):
    while True:
        clients_online = ""
        for client in clientnames:
            clients_online += client + "\n"
        clientsocket.send(b"||SERVER||REQUEST_LOGIN||AND||SERVER||ONLINE_USER|?|"+clients_online.encode('ascii'))
        login = clientsocket.recv(1024)
        try:
            print(login.decode('ascii').split("|?|")[1])
            name = login.decode('ascii').split("|?|")[1]
            if name in clientnames:
                clientsocket.send(b"||SERVER||LOGIN||FAILED||")
                logging.set(logging.get()+"\n"+"Connection attempt denied from: `"+str(addr)+"`, name: `"+name+"` at :"+getTime())
            else:
                break
        except IndexError:
            print("Invalid login.")
    clientsockets.append(clientsocket)
    clientnames.append(name)
    for client in clientnames:
        clients_online += client + "\n"

    for skt in clientsockets:
        skt.send(b"||SERVER||ONLINE_USER|?|"+clients_online.encode('ascii'))
    print("Connection from: " + str(addr)+ "at : "+getTime())
    logging.set(logging.get()+"\n"+"Connection from: `"+str(addr)+"`, name: `"+name+"` at : "+getTime())
    clients_name.set(clients_name.get()+"\n"+name+" : "+str(addr))
    tPool.add_task(clientsocket, name, clientsockets, root, task=dispatch_message)


def listener(serversocket, clientsocket, clientnames, root):
    while True:
        try:
            serversocket.listen()
            clientsocket, addr = serversocket.accept()
            tPool.add_task(serversocket, addr, clientnames, clientsocket, root, task=login)
        except:
            print("Server closed at : "+ getTime())
            break

def dispatch_message(skt, name, clientsockets, root):
    while True:
        try:

            msg = skt.recv(1024)
            msg = msg.decode('ascii')
            if msg == "":
                raise Exception("Connection closed.")

            if  b"||CLIENT||LOGIN||RESPONSE|?|" in msg.encode('ascii'):
                print("connection attempt denied from:"+name)
                logging.set(logging.get()+"\n"+"Duplicate connection attempt denied from: `"+str(skt.getpeername())+"`, name: `"+name+"` at : "+getTime())
                continue
            msg_send = name+": " + msg
            msg = getTime()+"\nfrom:" + name + " - message: " + msg
            logging.set(logging.get()+"\n"+msg)
            print(msg)
            for skt_out in clientsockets:
                skt_out.send(msg_send.encode('ascii'))
        except:
            clientsockets.remove(skt)
            clientnames.remove(name)
            print("Connection closed.")
            clients_inside = clients_name.get()
            clients_inside = clients_inside.replace(name+" : "+str(skt.getpeername()), "")
            clients_name.set(clients_inside)
            for skt_out in clientsockets:
                skt_out.send(b"||SERVER||ONLINE_USER|?|"+clients_inside.encode('ascii'))
            logging.set(logging.get()+"\n"+"Connection closed from: `"+str(skt.getpeername())+"`, name: `"+name+"` at : "+getTime())
            break


def closeServer(serversocket):
    serversocket.close()

    exit(0)

 # ======================================= START =======================================

tPool.add_task(serversocket, clientsockets, clientnames, root, task=listener)

root.mainloop()
