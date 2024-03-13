from typing import (Any, Dict)

from configuration import get_configuration

from getpass import getpass
from hashlib import sha512
from db_handler import (
    # Create
    create_default_tables,
    create_usr_db,
    # Read
    check_tables_exist,
    check_user_exist,
    # Update

    # Delete

)

class App:
    def __init__(self) -> None:
        """
            Load the configuration file and its content and run the app
        """
        self.config: Dict[str, Any] = get_configuration("configuration.toml")

    def main(self) -> None:
        """
            Main functionality of the app
        """
        try:
            choice = int(input("1- Log In\n2 - Sign Up\n"))
        except ValueError:
            print("[-] You must select an option")
            exit(1)
        match choice:
            case 1:
                self.log_in()
            case 2:
                self.sign_up()
            case _:
                print("Enter a valid option")
                exit(1)
    def log_in(self) -> None:
        """
            Functionality for Log In the platform
        """
        uname: str = input("Enter your username: ")
        if not uname:
            print("You must provide a username")
            exit(1)
        passwd: bytes = bytes(getpass(), encoding="utf-8")
        if passwd:
            if len(passwd) < 8:
                print("Password too short")
                exit(1)
            else:
                # Get the hexadecimal version of the hash
                passwd_hash: str = sha512(string=passwd).hexdigest()
                # data = get_users()
                if check_user_exist(uname=uname, passwd=passwd_hash,
                                    all_credentials=True):
                    print("[+] Logged In")
        else:
            print("You must provide a password")
            exit(1)
    def sign_up(self) -> None:
        """
            Functionality for Sign Up in the plaform
        """
        uname: str = input("Enter your username: ")
        if not uname:
            print("You must provide a username")
            exit(1)
        passwd: bytes = bytes(getpass(), encoding="utf-8")
        if passwd:
            if len(passwd) < 10:
                print("Password too short")
                exit(1)
            else:
                passwd_hash: str = sha512(string=passwd).hexdigest()
                create_usr_db(uname=uname, passwd=passwd_hash, is_staff=0)
                print("[+] Account created successfully, now Log In")
                exit(0)
        else:
            print("You must provide a password")
            exit(1)
if __name__ == "__main__":
    a = App()
    a.main()
