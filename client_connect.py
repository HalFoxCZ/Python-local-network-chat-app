import socket
import time


class CONNECT:
    @staticmethod
    def connect_to_server(server_port: int = 42069, max_port: int = 42099) -> socket.socket:
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_host = socket.gethostname()
                s.connect((server_host, server_port))
                break
            except:
                print("Port "+str(server_port)+" is not used")
                server_port += 1

                if server_port > max_port:
                    print("No ports available.")
                    exit(0)
            time.sleep(0.2)
        return s


