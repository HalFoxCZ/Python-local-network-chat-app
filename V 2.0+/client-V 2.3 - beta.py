import socket
import threading
import time
from threadpool import ThreadPool as tPool
import tkinter as tk

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_host = socket.gethostname()
server_port = 42069
s.connect(("DST22811", server_port))
server_addr = s.getpeername()

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            message = message.decode('ascii')

            set_chat_text.set(set_chat_text.get()+"\n"+message)
            print(message)

        except ConnectionResetError:
            print("Connection closed.")
            break

def send_message(message, s):
    print(message)
    s.sendall(message.encode('ascii'))

root = tk.Tk()
root.title("chat-app")
root.geometry("500x600")

set_chat_text = tk.StringVar()
set_chat_text.set("")
chat_text = tk.Label(
    root,
    textvariable=set_chat_text
)

input_user = tk.Text(
    root,
    height=1,
    width=20
)

send_button = tk.Button(
    root,
    text="Send",
    command=lambda: send_message(input_user.get("1.0", "end-1c"), s)
)

chat_text.grid(row=1, column=2000, columnspan=10)
input_user.grid(row=2, column=1, columnspan=5)
send_button.grid(row=2, column=6, columnspan=5)

tPool = tPool(50)
tPool.add_task(s, task=receive_messages)

root.mainloop()