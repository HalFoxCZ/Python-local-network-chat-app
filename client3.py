import socket
import threading
import time
from threadpool import ThreadPool as tPool

length = 20
sockets = []



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


            print(align_text("[server]", length, message))
            line_split(100)

        except ConnectionResetError:
            print("Connection closed.")
            break

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_host = socket.gethostname()
server_port = 42069
line_split(100)
s.connect((server_host, server_port))
server_addr = s.getpeername()

print(align_text("address", length, server_addr[0]))
print(align_text("port", length, server_addr[1]))
line_split(100)

msg = s.recv(1024)
print(align_text("[server]", length, msg.decode('ascii')))

tPool = tPool(50)

tPool.add_task(s, task=receive_messages)

while True:
    time.sleep(0.1)
    user_input = input("Enter your message: ")
    line_split(100)


    if user_input.lower() != 'exit':
        s.sendall(user_input.encode("ascii"))
    else:

        s.sendall("terminated...".encode("ascii"))

        s.close()

        break


