## This is a program to simulate a bank account with all its basic operations,
## (Still in development)
from sys import exit
from json import dumps, load
from random import randint
from os.path import exists
class BankAccount:
    def __init__(self):
        self.headline = None
        self.account_number = None
        self.password = None
        self.balance = None
    def create_account(self):
        headline = input("Enter A Headline: ")
        account_number = randint(1, 1001)
        password = input("Enter A Password: ")
        warning = ("Missing One Or More Parameters")
        if not headline:
            print(warning)
            exit(0)
        if not password:
            print(warning)
            exit(0)
        self.headline = headline
        self.account_number = randint(1, 1001)
        self.password = password
        with open("credentials.json", "a+") as file:
            file.write(dumps({"headline" : self.headline,
            "account_number" : self.account_number, "password" : self.password, 
            "balance" : None}, indent=4))
            file.write("\n")
        print("Your Account Has Been Created")
        exit(0)
    def log_in(self):
        headline = input("Headline: ")
        password = input("Password: ")
        if exists("credentials.json"):
            with open("credentials.json", "r+") as file:
                data = load(file)
            checks = 0
            for key, value in data.items():
                if headline in str(value):
                    checks += 1
                if password in str(value):
                    checks += 1
            if checks == 2:
                print("Succesfully Entered")
if __name__ == ("__main__"):
    app = BankAccount()
    election = input("Log In (1) or Sign Up (2)?: ")    
    if election == ("1"):
        app.log_in()
    if election == ("2"):
        app.create_account()
