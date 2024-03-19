import socket
import threading
import time
from threadpool import ThreadPool as tPool
import tkinter as tk

length = 20

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

            label_text.set(message)
            print(align_text("[server]", length, message))

        except ConnectionResetError:
            print("Connection closed.")
            break


def align_text(textBefore="", chars=10, text_after=""):
    length_original = len(textBefore)
    spaces = chars - length_original
    text_after = str(text_after)
    if spaces < 0:
        return textBefore + ": " + text_after
    else:
        return textBefore + "." * spaces + ":" + text_after


root = tk.Tk()
root.title("chat-app")
root.geometry("500x600")


label_text = tk.StringVar()
label_text.set("0")


label = tk.Label(
    root,
    textvariable=label_text,

)

port = tk.Label(
    root,
    text= align_text("address", length, server_addr[0])+"\n"+align_text("port", length, server_addr[1])
)
port.grid(row=0, column=2000, columnspan=10)
label.grid(row=1, column=2000, columnspan=10)






msg = s.recv(1024)
print(align_text("[server]", length, msg.decode('ascii')))

tPool = tPool(50)

def send_message(message, user_socket):
    user_socket.sendall(message.encode('ascii'))

chat_input = tk.Text(

    height=1,
    width=20

)

chat_input.grid(row=2, column=1, columnspan=5)
send_button = tk.Button(
    text="send",
    command=lambda: send_message(chat_input.get("1.0", "end-1c"), s)
)

send_button.grid(row=2, column=6, columnspan=5)
root.mainloop()
def looping(s):
    while True:

        if chat_input.get("1.0", "end-1c") != 'exit':
            s.sendall(user_input.encode("ascii"))
        else:

            s.sendall("terminated...".encode("ascii"))

            s.close()

            break


tPool.add_task(s, task=looping)
tPool.add_task(s, task=receive_messages)