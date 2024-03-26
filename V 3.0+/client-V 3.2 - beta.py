import socket
import threading
import time
from threadpool import ThreadPool as tPool
import tkinter as tk


server_port = 42069
while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_host = socket.gethostname()
        s.connect(("DST22811", server_port))
        break
    except:
        print("Port "+str(server_port)+" is not used")
        server_port += 1

        if server_port > 42099:
            print("No ports available.")
            exit(0)
            break
    time.sleep(0.2)

server_addr = s.getpeername()

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            elif message.decode('ascii') == "||SERVER||REQUEST_LOGIN||" or message.decode('ascii') == "||SERVER||LOGIN||FAILED||":
                login_label.grid(row=0, column=1, columnspan=1)
                login_button.grid(row=0, column=6, columnspan=2)
                close_button.grid(row=10, column=20, columnspan=5)
                chat_text.grid_forget()
                input_user.grid_forget()
                send_button.grid_forget()
                username_text.set("")
                username_label.grid()
            else:

                message = message.decode('ascii')

                set_chat_text.set(set_chat_text.get()+"\n"+message)
                print(message)

        except ConnectionResetError:
            print("Connection closed.")
            break

def send_message(message, s):
    input_user.delete("1.0", "end-1c")
    print(message)
    if "||CLIENT||LOGIN||RESPONSE|?|" in message:

        login_label.grid_forget()
        login_button.grid_forget()
        chat_text.grid(row=1, column=2000, columnspan=10)
        input_user.grid(row=2, column=1, columnspan=5)
        send_button.grid(row=2, column=6, columnspan=5)
        username_text.set(message.split("||CLIENT||LOGIN||RESPONSE|?|")[1])
        username_label.grid(row=0, column=0, columnspan=1)
    s.sendall(message.encode('ascii'))

root = tk.Tk()
root.title("chat-app")
root.geometry("700x900")

set_chat_text = tk.StringVar()
set_chat_text.set("")


username_text = tk.StringVar()
username_text.set("")
username_label = tk.Label(
    root,
    textvariable=username_text,
    height=1,
    width=20,
)


login_label = tk.Text(
    root,
    height=1,
    width=20
)

login_button = tk.Button(
    root,
    text="Login",
    command=lambda: send_message("||CLIENT||LOGIN||RESPONSE|?|"+login_label.get("1.0", "end-1c"), s)
)
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

close_button = tk.Button(
    root,
    text="Close",
    command=lambda: endApp(root, s)

)


def endApp(root, s):
    s.close()
    root.quit()
    root.destroy()


tPool = tPool(50)
tPool.add_task(s, task=receive_messages)

root.mainloop()