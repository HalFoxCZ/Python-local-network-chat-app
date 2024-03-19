import socket
import threading
import time
from threadpool import ThreadPool as tPool
import tkinter as tk

length = 20
sockets = []

root = tk.Tk()
root.title("chat-app")
root.geometry("500x600")


label_text = tk.StringVar()
label_text.set("0")


label = tk.Label(
    root,
    textvariable=label_text,

)
label.grid(row=1, column=2000, columnspan=10)



def line_split(chars=20):
    print("-" * chars)

def align_text(textBefore="", chars=10, text_after=""):
    length_original = len(textBefore)
    spaces = chars - length_original
    text_after = str(text_after)
    if spaces < 0:
        return textBefore + ": " + text_after
    else:
        return textBefore + "." * spaces + ":" + text_after

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            message = message.decode('ascii')

            label_text.set(message)
            print(align_text("[server]", length, message))
            line_split(100)

        except ConnectionResetError:
            print("Connection closed.")
            break

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_host = socket.gethostname()


server_port = 42069
line_split(100)
s.connect(("DST22812", server_port))
server_addr = s.getpeername()

print(align_text("address", length, server_addr[0]))
print(align_text("port", length, server_addr[1]))
line_split(100)

msg = s.recv(1024)
print(align_text("[server]", length, msg.decode('ascii')))

tPool = tPool(50)

tPool.add_task(s, task=receive_messages)


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
def looping():
    while True:

        if chat_input.get("1.0", "end-1c") != 'exit':
            s.sendall(user_input.encode("ascii"))
        else:

            s.sendall("terminated...".encode("ascii"))

            s.close()

            break


threading.Thread(target=looping).start()
