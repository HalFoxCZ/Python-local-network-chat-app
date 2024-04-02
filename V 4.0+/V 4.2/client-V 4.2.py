import socket
import threading
import time
from threadpool import ThreadPool as tPool
import tkinter as tk
from client_connect import CONNECT as ct
import datetime

server_port = 42069
s = ct.connect_to_server(server_port)
server_addr = s.getpeername()
print(s)

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            if "||SERVER||REQUEST_LOGIN||" in message.decode("ascii") or "||SERVER||LOGIN||FAILED||" in message.decode('ascii') or "||SERVER||ONLINE_USER|?|" in message.decode('ascii'):

                if "||SERVER||REQUEST_LOGIN||" in message.decode("ascii") or "||SERVER||LOGIN||FAILED||" in message.decode('ascii'):
                    login_label.grid(row=1, column=0, )
                    login_button.grid(row=2, column=0, )
                    close_button.grid(row=0, column=0, )
                    chat_text.grid_forget()
                    input_user.grid_forget()
                    send_button.grid_forget()
                    username_text.set("")
                    username_label.grid()
                    users_label.grid()
                if "||SERVER||ONLINE_USER|?|" in message.decode('ascii'):
                    users.set("users:\n"+message.decode('ascii').split("||SERVER||ONLINE_USER|?|")[1])
            else:

                message = message.decode('ascii')
                time = datetime.datetime.now().strftime("%H:%M:%S")
                set_chat_text.set(set_chat_text.get()+"\n"+time+"--"+message)
                print(message)

        except:
            print("Connection closed.")
            break

def send_message(message, s):
    input_user.delete("1.0", "end-1c")
    print(message)
    if "||CLIENT||LOGIN||RESPONSE|?|" in message:
        print(message)
        if message == "||CLIENT||LOGIN||RESPONSE|?|":
            return
        login_label.grid_forget()
        login_button.grid_forget()
        chat_text.grid(row=1, column=0)
        input_user.grid(row=2, column=0)
        send_button.grid(row=3, column=0)
        username_text.set(message.split("||CLIENT||LOGIN||RESPONSE|?|")[1])
        username_label.grid(row=0, column=2)
        users_label.grid(row=0, column=3)
    if message == "":
        pass
    s.sendall(message.encode('ascii'))


root = tk.Tk()
root.title("chat-app")
root.geometry("700x900+%d+%d" % (root.winfo_screenheight(), 0))

set_chat_text = tk.StringVar()
set_chat_text.set("")

root.configure(background="#222")



username_text = tk.StringVar()
username_text.set("")
username_label = tk.Label(
    root,
    textvariable=username_text,
    height=1,
    width=20,
    font=('Comic Sans MS', 12, 'bold italic')

)


login_label = tk.Text(
    root,
    height=1,
    width=20,
    borderwidth=2,
    font=('Comic Sans MS', 12, 'bold italic')

)

login_button = tk.Button(
    root,
    text="Login",
    command=lambda: send_message("||CLIENT||LOGIN||RESPONSE|?|"+login_label.get("1.0", "end-1c"), s),
    font=('Comic Sans MS', 12, 'bold italic')

)
chat_text = tk.Label(
    root,
    textvariable=set_chat_text,
    height=25,
    width=50,
    anchor="nw",
    justify="left",
    font=('Comic Sans MS', 12, 'bold italic')

)

input_user = tk.Text(
    root,
    height=1,
    width=20,
    font=('Comic Sans MS', 12, 'bold italic')

)

send_button = tk.Button(
    root,
    text="Send",
    command=lambda: send_message(input_user.get("1.0", "end-1c"), s),
    font=('Comic Sans MS', 12, 'bold italic')

)

close_button = tk.Button(
    root,
    text="Close",
    command=lambda: endApp(root, s),
    font=('Comic Sans MS', 12, 'bold italic')

)

users = tk.StringVar()
users.set("")

users_label = tk.Label(
    root,
    textvariable=users,
    font=('Comic Sans MS', 12, 'bold italic')

)


def endApp(root, s):
    s.close()
    root.quit()
    root.destroy()
    exit(0)

tPool = tPool(50)
tPool.add_task(s, task=receive_messages)
root.mainloop()


