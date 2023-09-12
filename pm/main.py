from argparse import ArgumentParser
from database import Database
from string import punctuation
from time import sleep
from signal import (signal,
                    SIGINT,
                    SIGTSTP)

class App:
    def __init__(self):
        signal(SIGINT, self.signal_handler)
        signal(SIGTSTP, self.signal_handler)
        self.get_arguments()
        self.main()
    def main(self):
        self.database = Database()
        check_db_results = self.database.check_db_name(db_name=self.args.db_name[0])
        if check_db_results == "is_valid":
            print("Welcome to the password manager")
            self.database.create_database(db_name=self.args.db_name[0])
            self.database.create_main_table(db_name=self.args.db_name[0])
            print("[+] Passwords Database Created Successfully", end="\n\n")
            # self.user_option = input("[?] Do you want to create a record? [Y/N] -> ").upper()
            while True:
                try:
                    user_option = int(input("""1- Create Record
2- Delete Record
3- Read Records\n"""))
                    if user_option == 1:
                        self.get_record()
                        break
                    if user_option == 2:
                        pass
                    if user_option == 3:
                        self.delete_record()
                    else:
                        break
                except ValueError:
                    print("[!] The option must be a number not letter or punctuation symbol")
                    break
                except Exception as f:
                    print("[!] An unexpected error has ocurred")
                    print(f)
                    break
            exit(code=0)
        if check_db_results == "there_is_an_equal":
            print("[!] There is an existing database with the same name, it will be opened...")
            self.checking_table_results = self.database.check_db_integrity(db_name=self.args.db_name[0])
            if self.checking_table_results == "is_valid":
                print("[+] The content of the database is not altered")
                while True:
                    try:
                        user_option = int(input("""1- Create Record
2- Delete Record
3- Read Records\n"""))
                        if user_option == 1:
                            self.get_record()
                        if user_option == 2:
                            self.delete_record()
                    except ValueError:
                        print("[!] The option must be a number not letter or punctuation symbol")
                        break
                    except Exception as _:
                        print("[!] An unexpected error has ocurred")
                        #print(_)
                        break
            else:
                print("[-] The content of the database is altered")
                answer = input("Do you want to delete that database? [Y/N]: ").upper()
                #if answer == "Y":

            exit(code=0)

        if check_db_results == "is_invalid":
            print("[-] There seems to be a file or folder with the same name, so you cannot create the database with that name")
            exit(code=1)

    def get_record(self):
        user_username = str(input("Please enter your registry username: "))
        user_password = str(input("Please enter your registry password: "))
        print("[+] Creating Record...")
        self.database.create_record(db_name=self.args.db_name[0],
                                    username=user_username,
                                    password=user_password)
        print("[+] Record created successfully")

    def delete_record(self):
        data = self.database.get_data_from_db(self.args.db_name[0])
        print(" ", 46 * "⎽", sep="")
        print(" ", "|", 10 * " ", "|", 16 * " ", "|", 16 * " ", "|", sep="")
        print(" ", "|", "    ID    ", "|", 4 * " ", "USERNAME", 4 * " ", "|", 4 * " ", "PASSWORD", 4 * " ", "|", sep="")
        print(" ", "|", 10 * " ", "|", 16 * " ", "|", 16 * " ", "|", sep="")
        print(" ", 46 * "⎼", sep="")
        for dataset in data:
            encrypted_pass = len(dataset[2]) * "*"
            print(" ", "|", dataset[0], (10 - len(str(dataset[0]))) * " ", "|", dataset[1], (16 - len(str(dataset[1]))) * " ", "|", encrypted_pass, (16 - len(encrypted_pass)) * " ", "|", sep="", flush=True)
#s    def valid_user_input(self, input_data):
#        for char in input_data:
#            if char in punctuation:
#                return False
#        else:
#            return True
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
        exit(code=0)
if __name__ == "__main__":
    app = App()