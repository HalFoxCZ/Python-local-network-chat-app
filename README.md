
**<h1>CHAT APP</h1>**

**Description:**
This is a chat app that allows users to chat with each other.

**<h2>Installation: </h2>**
> - **Server:**
> > - Download the server from the repository.
> > - Run the server.
> > - Server is now running and ready to accept connections from uo to 50 clients.
> > - can be edited by increasing mumber in the **SERVER** file on line `tPool = tPool(100)` . Each client need 2 threads, soo  that needs to be in incremeants of 2.
> > - Each server is compatible with the same main version of the client.
> > - Server is ***not compatible*** with clients from different main versions.
> > - <u>Server is compatible with clients from different subversions.</u>

> - **Client:**
> >- Download the client from the repository.
> > - If server is running, run the client.
> > - If server is not running, run the server first and then the client.
> > - Client is now running and connected to the server.
> > - Each client is compatible with the same main version of the server.
> > - Client is ***not compatible*** with servers from different main versions.
> > - Client is compatible with servers from different subversions.
> > - *<b><u>All users have to be on same local network to connect to the server.</b></u>*

- **<h2>Features:</h2>**
> - Features are only for the client.
> - Any servers above, including ***V 3.2 - alpha*** have GUI loging.
> - Any server below ***V 3.1 - alpha*** have only terminal loging.
> - <h3>V 1.4 - beta:</h3>
 > > - User can send messages to other users.
> > - ***Incompatible*** with server ***V 3.1 - alpha*** and above.
> > - Chat ***doesn't*** show who sent the message.
> > - Can be closed by typing "exit" in the chat.
> > - Really outdated, not recommended to use.
> > - **Server is not able to download, unuseable.**

>  - <h3>V 2.3 - beta:</h3>
> > - User can send messages to other users.
> > - Messages are displayed in the chat window.
> > - Messages have user adress from witch were sent.
> > - Incompatible with server ***V 3.1 - alpha*** and above.
> > - All versions above **V 2.3 - beta*** have removed close window exit with typing "exit" in chat.
> > - Outdated, not recommended to use, but server is still avaible to download and use.
        
>  - <h3>V 3.1 - alpha:</h3>
> > - User can send messages to other users.
> > - Messages are displayed in the chat window.
> > - Messages have user`s name who sent them.
> > - Compatible with server ***V 3.1 - alpha*** and above.

>  - <h3>V 3.2 - alpha:</h3>
> > - Same as ***V 3.1 - alpha***.
> > - Added close window button to close the app.
> > - User`s name is displayed in the chat window.
> > - Compatible with server ***V 3.1 - alpha*** and above.

- **<h2>SERVER functions:</h2>**
> - <h3>variables:</h3>
> > - `tPool = tPool(100)` - number of threads that server can handle. Each client needs 2 threads.
> > - `serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)` - creates a socket for the server.
> > - `host = socket.gethostname()` - gets the host name of the server.
> > - `port = 42069` - port on which the server is running. Automaticly will be change up to 30 numbers higher if this is used.
> > - `clientsockets = []` - list of all client sockets that are conected.
> > - `clientnames = []` - list of all client names that are conected.
> > 
> - <h3>functions:</h3>
>
> > ```
> >   def listener(serversocket, clientsocket, clientnames):
> >   while True:
> >       serversocket.listen()
> >       clientsocket, addr = serversocket.accept()
> >       tPool.add_task(serversocket, addr, clientnames, clientsocket, task=login)
> >  ```
> >  - listens for new connections and sends them to login function.




- **<h2>Sources:</h2>**
> - the threadpool (threadpool.py) was coded by [Kryštof Fábel](https://github.com/fabelkr)