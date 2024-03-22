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
    get_user_info,
    # Update
    # Delete
)
# For colorize text
from colorama import Fore
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
            choice = int(input(Fore.LIGHTGREEN_EX + ("1- Log In\n"
                "2- Sign Up\n")))
            uname: str = input(Fore.LIGHTGREEN_EX + "Enter your username: ")
            # uname = "ssynaptic"
            if not uname:
                print(Fore.LIGHTRED_EX + "[-] You must provide a username")
                exit(1)
            passwd: bytes = bytes(getpass(), encoding="utf-8")
            # passwd = bytes("dXrker@f0x", encoding="utf-8")
            if passwd:
                if len(passwd) < 8:
                    print(Fore.LIGHTRED_EX + "[-] Password too short")
                    exit(1)
                else:
                    # Convert hash to a hexadecimal string
                    passwd_hash: str = sha512(string=passwd).hexdigest()
            else:
                print(Fore.LIGHTRED_EX + "[-] You must provide a password")
                exit(1)
        except ValueError:
            print(Fore.LIGHTRED_EX + "[-] You must select an option")
            exit(1)
        match choice:
            case 1:
                self.log_in(uname=uname, passwd_hash=passwd_hash)
            case 2:
                self.sign_up(uname=uname, passwd_hash=passwd_hash)
            case _:
                print(Fore.LIGHTRED_EX + "[-] Enter a valid option")
                exit(1)
    def log_in(self, uname: str, passwd_hash: str) -> None:
        """
            Functionality for Log In the platform
        """
        if check_user_exist(uname=uname, passwd=passwd_hash,
                            all_credentials=True):
            print("[+] Logged In.")
            self.display_home_page(uname=uname, passwd_hash=passwd_hash)
            # self.user = (uname, passwd_hash)
        else:
            print("[-] Wrong username and/or password.")
    def sign_up(self, uname: str, passwd_hash: str) -> None:
        """
            Functionality for Sign Up in the plaform
        """
        create_usr_db(uname=uname, passwd=passwd_hash, account_type=0)
        print("[+] Account created successfully, now Log In")
    def display_home_page(self, uname: str, passwd_hash: str):
        """
            Select the type of home page depending on the type
            of user account with which you are logged in
        """
        self.user: Tuple(Any) = get_user_info(uname=uname,
                                         passwd_hash=passwd_hash)
        # Display a menu with different options depending on the
        # type of the user
        match self.user[5]:
            case 0:
                self.usr_zero_home_page()
            case 1:
                self.usr_one_home_page()
            case 2:
                self.usr_two_home_page()
    def usr_zero_home_page(self):
        """
            Home page for a normal user on the library
        """
        menu: str = ("Welcome user\n"
                     # "1- Trending\n"
                     "2- Find books\n"
                     "3- Borrows books\n"
                     "4- My favorites\n")
        match int(input(menu)):
            case 2:
                pass
            case 3:
                pass
            case 4:
                pass
    def usr_one_home_page(self):
        """
            Home page for the staff accounts on the library
        """
#         menu: str = ("Welcome user\n"
#                      "1- Trending\n"
#                      "2- Find books\n"
#                      "3- Borrows books\n"
#                      "4- My favorites\n")
        menu = ("Welcome user\n"
                "1- Register book\n")

        match int(input(menu)):
            case 1:
                pass
            case 2:
                pass
            case 3:
                pass
            case 4:
                pass
    def usr_two_home_page(self):
        """
            Home page for the full access accounts on the library
        """
        pass
if __name__ == "__main__":
    a = App()
    a.main()
