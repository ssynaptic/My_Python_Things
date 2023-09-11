from argparse import ArgumentParser
from database import Database
from string import punctuation
from time import sleep
from signal import (signal,
                    SIGINT,
                    SIGTSTP)
class App:
    def __init__(self):
        # print(signal.valid_signals())
        signal(SIGINT, self.signal_handler)
        signal(SIGTSTP, self.signal_handler)
        self.get_arguments()
        self.main()
    def main(self):
        self.database = Database()
        self.check_db_results = self.database.check_db_name(db_name=self.args.db_name[0])
        if self.check_db_results == "is_valid":
            print("Welcome to the password manager")
            self.database.create_database(db_name=self.args.db_name[0])
            self.database.create_main_table(db_name=self.args.db_name[0])
            print("[+] Passwords Database Created Successfully", end="\n\n")
            # self.user_option = input("[?] Do you want to create a record? [Y/N] -> ").upper()
            while True:
                self.user_option = int(input("""1- Create Record
2- Delete Record
3- Read Records\n"""))
                if self.user_option == 1:
                    self.get_record()
                    break
                else:
                    break
            exit(code=0)
        if self.check_db_results == "there_is_an_equal":
            # print("[-] That is not a valid name, enter another")
            print("[!] There is an existing database with the same name, it will be opened...")
            print(self.args.db_name[0])
            self.cresults = self.database.check_db_integrity(db_name=self.args.db_name[0])
            print(self.cresults)
            exit(code=1)

    def get_record(self):
        self.user_username = str(input("Please enter your registry username: "))
        self.user_password = str(input("Please enter your registry password: "))
        print("[+] Validating...")
        sleep(1)
        self.results = tuple(map(self.valid_user_input, (self.user_username, self.user_password)))

        if self.results[0] == True and self.results[1] == True:
            print("[+] Success")
            print("[+] Creating Record...")
            self.database.create_record(db_name=self.args.db_name[0],
                                        username=self.user_username,
                                        password=self.user_password)
            sleep(1)
            print("[+] Success")
        else:
            print("[-] Bad Input")
            exit(code=1)
    def valid_user_input(self, input_data):
        for char in input_data:
            if char in punctuation:
                return False
        else:
            return True
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
        self.args = self.parser.parse_args()

    def signal_handler(self, signum, frame):
        print("Exiting...")
        sleep(1)
        exit(code=1)
if __name__ == "__main__":
    app = App()