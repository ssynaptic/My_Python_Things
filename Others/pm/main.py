# This is a password manager for terminal written in Python
# VERSION: 1.0.0

from argparse import ArgumentParser
from database import Database
from db_crypto import CryptoHandler
from getpass import getpass
from string import punctuation
from time import sleep
from signal import (signal,
                    SIGINT,
                    SIGTSTP)
from colorama import (init,
                      Fore)
class App:
    def __init__(self):
        signal(SIGINT, self.signal_handler)
        signal(SIGTSTP, self.signal_handler)
        self.get_arguments()
        self.main()
    def main(self):
        self.database = Database()
        self.crypto_handler = CryptoHandler()
        self.database_name = self.args.db_name[0]
        # check_db_results = self.database.check_db_name(db_name=self.args.db_name[0])
        check_db_results = self.database.check_db_name(db_name=self.database_name)
        if check_db_results == "is_valid":
            print("Welcome to the password manager")
            self.database.create_database(db_name=self.database_name)
            self.database.create_main_table(db_name=self.database_name)
            self.given_db_password = getpass(prompt=Fore.WHITE + "Enter the password to encrypt the DB: ")
            if not self.given_db_password:
                print(Fore.LIGHTRED_EX + "[-] You must provide a password to encrypt the database")
                exit(code=1)
            print(Fore.LIGHTGREEN_EX + "[+] Passwords Database Created Successfully", end="\n\n")
            while True:
                try:
                    user_option = int(input("""1- Create Record
2- Delete Record
3- Read Records
4- Exit\n"""))
                    if user_option == 1:
                        self.get_record()
                        continue
                    if user_option == 2:
                        self.delete_record()
                        continue
                    if user_option == 3:
                        self.print_table()
                        continue
                    if user_option == 4:
                        print(Fore.WHITE + "Exiting...")
                        break
 #                   else:
 #                       continue
                except ValueError:
                    print("[!] The option must be a number not letter or punctuation symbol")
                    break
                except Exception as f:
                    print("[!] An unexpected error has ocurred")
                    print(f)
                    break
            exit(code=0)
        if check_db_results == "there_is_an_equal":
            print(Fore.LIGHTYELLOW_EX + "[!] There is an existing database with the same name, it will be opened...")
            self.checking_table_results = self.database.check_db_integrity(db_name=self.database_name)
            if self.checking_table_results == "is_valid":
                print(Fore.LIGHTGREEN_EX + "[+] The content of the database is not altered")
                while True:
                    try:
                        user_option = int(input("""1- Create Record
2- Delete Record
3- Read Records
4- Exit\n"""))
                        if user_option == 1:
                            self.get_record()
                            continue
                        if user_option == 2:
                            self.delete_record()
                            continue
                        if user_option == 3:
                            self.print_table()
                            continue
                        if user_option == 4:
                            print(Fore.WHITE + "Exiting...")
                            # exit(code=0)
                            break
#                        else:
#                            continue
                    except ValueError:
                        print(Fore.RED + "[!] The option must be a number not letter or punctuation symbol")
                        continue
#                    except Exception as _:
#                        print("[!] An unexpected error has ocurred")
                        # print(_)
#                        break
            else:
                print(Fore.LIGHTRED_EX + "[-] The content of the database is altered")
                exit(code=1)

            exit(code=0)

        if check_db_results == "is_invalid":
            print("[-] There seems to be a file or folder with the same name, so you cannot create the database with that name")
            exit(code=1)

    def get_record(self):
        user_username = str(input("Please enter your registry username: "))
        user_password = str(input("Please enter your registry password: "))
        print(Fore.LIGHTYELLOW_EX + "[!] Creating Record...")
        if len(user_username) >= 5 and len(user_password) >= 10:
            self.database.create_record(db_name=self.database_name,
                                        username=user_username,
                                        password=user_password)
            print(Fore.LIGHTGREEN_EX + "[+] Record created successfully")
        else:
            print(Fore.LIGHTRED_EX + "[!] Enter a longer username and/or password")

    def delete_record(self):
        self.print_table()
        records_ids = self.database.get_ids_from_db(db_name=self.database_name)
        records_ids = tuple(rid[0] for rid in records_ids)
        if not records_ids:
            pass
        else:
            given_user_id = int(input("Enter the ID: "))
            if given_user_id not in records_ids:
                print(Fore.LIGHTRED_EX + "[-] Invalid ID")
            else:
                self.database.delete_record(db_name=self.database_name,
                                            record_id=given_user_id)
                print(Fore.LIGHTGREEN_EX + "[+] Successfully Deleted")

    def print_table(self):
        data = self.database.get_data_from_db(db_name=self.database_name)
        print(" ", 46 * (Fore.LIGHTYELLOW_EX + "⎽"), sep="")
        print(" ", Fore.LIGHTGREEN_EX + "|", 10 * " ", Fore.LIGHTGREEN_EX + "|", 16 * " ", Fore.LIGHTGREEN_EX + "|", 16 * " ", Fore.LIGHTGREEN_EX + "|", sep="")
        print(" ", Fore.LIGHTGREEN_EX + "|", Fore.WHITE + "    ID    ", Fore.LIGHTGREEN_EX + "|", 4 * " ", Fore.WHITE + "USERNAME", 4 * " ", Fore.LIGHTGREEN_EX + "|", 4 * " ", Fore.WHITE + "PASSWORD", 4 * " ", Fore.LIGHTGREEN_EX + "|", sep="")
        print(" ", Fore.LIGHTGREEN_EX + "|", 10 * " ", Fore.LIGHTGREEN_EX + "|", 16 * " ", Fore.LIGHTGREEN_EX + "|", 16 * " ", Fore.LIGHTGREEN_EX + "|", sep="")
        print(" ", 46 * (Fore.LIGHTYELLOW_EX + "⎼"), sep="")

        if data:
            for dataset in data:
                encrypted_pass = len(dataset[2]) * "*"
                print(" ", Fore.LIGHTGREEN_EX + "|", dataset[0], (10 - len(str(dataset[0]))) * " ", Fore.LIGHTGREEN_EX + "|", dataset[1], (16 - len(str(dataset[1]))) * " ", Fore.LIGHTGREEN_EX + "|", encrypted_pass, (16 - len(encrypted_pass)) * " ", Fore.LIGHTGREEN_EX + "|", sep="", flush=True)
            return data
        else:
            print("", Fore.LIGHTYELLOW_EX + "[!] No records to display")

    def get_arguments(self):
        self.parser = ArgumentParser()
        self.parser.add_argument("-n",
                                 "--name",
                                 action="store",
                                 nargs=1,
                                 default=None,
                                 type=str,
                                 required=True,
                                 help="Database Name",
                                 metavar="<DB_NAME>",
                                 dest="db_name")
        self.parser.add_argument("")
        self.args = self.parser.parse_args()

    def signal_handler(self, signum, frame):
        print("Exiting...")
        sleep(1)
        exit(code=0)
if __name__ == "__main__":
    init(autoreset=True)
    app = App()