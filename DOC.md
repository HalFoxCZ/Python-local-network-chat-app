<h1 style="text-align: center; text-decoration: underline">DOCUMENTATION</h1>


<h2>CLIENT:</h2>
> <h3>functions:</h3>
> > ```
> > def receive_messages(client_socket: socket.socket):
> >     while True:
> >        try:
> >            message = client_socket.recv(1024)
> >            if not message:
> >                break
> >            elif "||SERVER||REQUEST_LOGIN||" in message.decode('ascii') or "||SERVER||LOGIN||FAILED||" in message.decode('ascii') or "||SERVER||ONLINE_USER|?|" in message.decode('ascii'):
> >                if "||SERVER||REQUEST_LOGIN||" in message.decode('ascii') or "||SERVER||LOGIN||FAILED||" in message.decode('ascii'):
> >                    login_label.grid(row=0, column=1, columnspan=1)
> >                    login_button.grid(row=0, column=6, columnspan=2)
> >                    close_button.grid(row=10, column=20, columnspan=5)
> >                    chat_text.grid_forget()
> >                    input_user.grid_forget()
> >                    send_button.grid_forget()
> >                    username_text.set("")
> >                    username_label.grid()
> >                if "||SERVER||ONLINE_USER|?|" in message.decode('ascii'):
> >                    users = "Online users:" + message.decode('ascii').split("||SERVER||ONLINE_USER|?|")[1]
> >                    online_users.set(users)
> >            else:
> >                message = message.decode('ascii')
> >                set_chat_text.set(set_chat_text.get()+"\n"+message)
> >                print(message)
> >        except ConnectionResetError:
> >            print("Connection closed.")
> >            break
> >
> >``` 
> > this script receive messages from server, and checks if they contain text defined for special actions or requests, such as '||SERVER||REQUEST||LOGIN' or '||SERVER||LOGIN||FAILED||'. If message like this is received from server,it won't be displayed and instead the script will do or call corresponding task or function.
> 
> >```
> >def send_message(message: str, s: socket.socket):
> >       input_user.delete("1.0", "end-1c")
> >    print(message)
> >    if "||CLIENT||LOGIN||RESPONSE|?|" in message:
> >
> >        login_label.grid_forget()
> >        login_button.grid_forget()
> >        chat_text.grid(row=1, column=2000, columnspan=10)
> >        input_user.grid(row=2, column=1, columnspan=5)
> >        send_button.grid(row=2, column=6, columnspan=5)
> >        username_text.set(message.split("||CLIENT||LOGIN||RESPONSE|?|")[1])
> >        username_label.grid(row=0, column=0, columnspan=1)
> >    s.sendall(message.encode('ascii'))
> >```
> > This script takes message from user's input and checks for
> '||CLIENT||LOGIN||RESPONSE|?|' which is sent by login button in lambda function. If the user sends this message, nothing else will happen since it only adds other components into the window, and because they are 
> already there, nothing changes at all.
> > The server then ignores this message, and only logs  it as a denied attempt for logging.
> 
> <h3>Rest of code:</h3>
> >Rest of the code is mainly responsible for the GUI, and connecting to the server by using own CONNECT class.

 <h2>CONNECT Class:</h2>
> > ```
> > class CONNECT:
> >    def connect_to_server(self, server_port: int = 42069, max_port: int = 42099) -> socket.socket:
> >        while True:
> >            try:
> >                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
> >                server_host = socket.gethostname()
> >                s.connect((server_host, server_port))
> >                break
> >            except:
> >                print("Port "+str(server_port)+" is not used")
> >                server_port += 1
> >                if server_port > max_port:
> >                    print("No ports available.")
> >                    exit(0)
> >            time.sleep(0.2)
> >        return s
> > ```
> > This is basically a while loop that tries connect to the server, and when it connects or runs out of possible ports (means the max port value is reached) it stops and returns the socket if connection or exit(0) if runs out of ports.
> 
 <h2>Threadpool: </h2>
> > ```
> > class ThreadPool:
> >     threads = []
> >     thread_count = 0
> >     def __init__(self, thread_count):
> >         self.thread_count = thread_count
> >         self.threads = [th.Thread() for _ in range(thread_count)]
> >     def add_task(self, *args, task):
> >         for thread in self.threads:
> >             if not thread.is_alive():
> >                 thread = th.Thread(target=task, args=args)
> >                 thread.start()
> >                 break
> >         else:
> >             print("All threads are busy. Please wait.")
> >     def wait_completion(self):
> >         for i in range(self.thread_count):
> >             self.threads[i].join()
> > ```
> > I have genuinely no idea how it works, it was help from [Kryštof Fábel](https://github.com/opikolim) as reward for helping him find out that
> > he swapped two variables, and it started working then.
> 
 <h2>SERVER</h2>
> <h3> Functions: </h3>
> note: accidentally pasted outdated version without GUI support, but in code of V4.0 and above is GUI setup completed.
> > ```
> > def listener(serversocket, clientsocket, clientnames):
> >     while True:
> >         serversocket.listen()
> >         clientsocket, addr = serversocket.accept()
> >         tPool.add_task(serversocket, addr, clientnames, clientsocket, task=login) 
> > ```
> > listens for client connections, if it gets connection it creates new task login
> 
> > ```
> >  def login(serversocket, addr, clientnames, clientsocket):
> >     while True:
> >         clients_online = ""
> >         for client in clientnames:
> >             clients_online += client + "\n"
> >         clientsocket.send(b"||SERVER||REQUEST_LOGIN||AND||SERVER||ONLINE_USER|?|"+clients_online)
> >         login = clientsocket.recv(1024)
> >         try:
> >             print(login.decode('ascii').split("|?|")[1])
> >             name = login.decode('ascii').split("|?|")[1]
> >             if name in clientnames:
> >                 clientsocket.send(b"||SERVER||LOGIN||FAILED||")
> >             else:
> >                 break
> >         except IndexError:
> >             print("Invalid login.")
> >     clientsockets.append(clientsocket)
> >     clientnames.append(name)
> >     print("Connection from: " + str(addr))
> >     tPool.add_task(clientsocket, name, clientsockets, task=dispatch_message)
> > ```
> > It sends list of currently online users from the moment the app was launched (too lazy to make it realtime) and 
> > also asks for clients username. when it receives username that is not on the list it adds it to lists of names and 
> > addresses, logs who logged in with address and username, and then creates dispatch message thread for the client
> >
> > ```
> > def dispatch_message(skt, name, clientsockets):
> >     while True:
> >         try:
> >             msg = skt.recv(1024)
> >             msg = msg.decode('ascii')
> >             if  b"||CLIENT||LOGIN||RESPONSE|?|" in msg.encode('ascii'):
> >                 print("connection attempt denied from:"+name)
> >                 continue
> >             msg_send = name+": "+msg
> >             msg = "from:"+name+" - message: "+ msg
> >             print(msg)
> >             for skt_out in clientsockets:
> >                 skt_out.send(msg_send.encode('ascii'))
> >         except:
> >             clientsockets.remove(skt)
> >             clientnames.remove(name)
> >             print("Connection closed.")
> >             break
> > ```
> > This function dispatches messages from users, and also checks if he is still 
> connected by try except statement. if it gets exception, it removes user from lists, and logs that user 
> disconnected
> > If it founds the '||CLIENT||LOGIN||RESPONSE|?|' in the message, it logs that user tried logging again, and denies sending this message, no matter what is there more.
> > <h3>Rest of code:</h3>
> > the rest of code is just binding the connection, and setting up GUI of Tkinter nodule
> 
<h2>NOTES:</h2>
> **Versions bellow 3.0** : outdated, first attempts and are not meant to be used. version of 2.x are posible to use, but they are a bit tricky to use, and needs a lot of tweaking
>
> **Versions 3.x** : Those versions are good to use, but still have some bugs, and are not fully optimized
> 
> **Versions 4.x** : Newes versions, that are fine to use, and I hope should work without any problems (I wasnt able to test them since my parrent issues with my father
> about admin prilages on my pc and etc.). Any major bugs found in 4.x should and will be 
> repaired in versions 5.x, and all minor bugs will be fixed in versions 6.x
> <h3>Plans for future versions:</h3>
> 
> **versions 5.x** : Those versions would have more optimized user GUI, and add block feature soo you can block annoying peoples.
> That means annother local file for cleint that will contain blocked users and for how logn they are block
> 
> **versions 6.x** : those versions would have more optimized, and would fix minor bugs from 4.x and major bugs from 6.x. 
> Also would be added ban funtion 
> on server GUI soo admins can permanently or temporaly ban peoples.
> That would mean there would be new file tha will contain server blocked peoples, and if its temporaly bad then how long 
> they have to wait to be able to again connect. This would be send to the user who tries to connect and is banned.
