import socket

length = 20

def line_split(chars=20):
    print("-" * chars)

def align_text(text_before="", chars=10, text_after=""):
    length_original = len(text_before)
    spaces = chars - length_original
    text_after = str(text_after)
    if spaces < 0:
        return text_before + ": " + text_after
    else:
        return text_before + "." * spaces + ": " + text_after

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname() # Get server hostname or IP address from user
port = 42069

line_split(100)
s.connect((host, port))
addr = s.getpeername()

print(align_text("address", length, s.getpeername()[0]))
print(align_text("port", length, s.getpeername()[1]))
line_split(100)

msg = s.recv(1024)
s.send(("Hello server!").encode())
s.send(("Hello server!").encode())
s.send(("Hello server!").encode())

print(align_text("[server]", length, msg.decode('ascii')))
print(align_text("[server]", length, msg.decode('ascii')))
print(align_text("[server]", length, msg.decode('ascii')))

