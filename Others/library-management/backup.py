from configuration import get_configuration
from argparse import ArgumentParser
from argparse import Namespace as ArgNamespace
from typing import (Any, Dict)
from getpass import getpass
from re import findall as re_findall
from hashlib import sha256
import db_handler
class App:
    def __init__(self, configuration: Dict[str, Any]):
        self.config = configuration
    
    def create_account(self, email, password) -> None:
        hash_ = sha256(password)
class AppController:
    """
    A class responsible for setting up the program and running
    the application.
    """
    def __init__(self) -> None:
        """
            Get the command line options and arguments, load the application configuration and initialize it.
        """
        self.args: Dict[str, Any] = self.get_arguments()
        self.configuration: ArgNamespace = get_configuration(self.args.config_path)
        self.app: App = App(configuration=self.configuration)
        self.main()
    def main(self) -> None:
        """
            Generate the user interface.
        """
        print(Fore.LIGHTGREEN_EX + "Welcome user, would yo like to:")
        print(Fore.LIGHTYELLOW_EX + "1- Log In")
        print(Fore.LIGHTYELLOW_EX + "2- Sign Up")
        try:
            user_choice: int = int(input())
        except ValueError:
            print(Fore.LIGHTRED_EX + "[-] Invalid Input. Exiting...")
            exit(1)
        match user_choice:
            case 1:
                print("Logging Up")
            case 2: 
                print("Enter your email: ", end="")
                user_email: str = input()
                if not user_email:
                    print(Fore.LIGHTRED_EX + "[-] You must provide an email")
                    exit(1)
                is_email_valid: bool = self.validate_email(user_email)
                if is_email_valid:
                    user_passwd: str = getpass()
                    if not user_passwd:
                        print(Fore.LIGHTRED_EX + "You must provide a password.")
                        exit(1)
                    else:
                        self.app.create_account(user_email, user_passwd)
                else:
                    print("The email is invalid, exiting")
                    exit(1)
            case _:
                print(Fore.RED + "[-] Please select a valid option")
                exit(1)
    def get_arguments(self) -> ArgNamespace:
        """
            Get the command line options and arguments
        """
        parser: ArgumentParser = ArgumentParser(
                    prog="Library Management Systen",
                    description="An application written in Python for manage any library",
                    epilog="Hopefully this program will be useful and complete for you")
        parser.add_argument("--config",
                            action="store",
                            default="configuration.toml",
                            dest="config_path",
                            help="Specify the configuration file for the program",
                            metavar="<FILE>",
                            nargs=1,
                            required=False,
                            type=str)
        args: ArgNamespace = parser.parse_args()
        return args
    def validate_email(self, email: str, /) -> bool:
        """
            Perform the email validation using a Regex and
            return True of False if the email is valid or
            invalid respectively
        """
        pattern: str = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        matches = re_findall(pattern, email)
        if matches:
            return True
        else:
            return False

if __name__ == "__main__":
    AppController()
