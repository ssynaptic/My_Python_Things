from argparse import ArgumentParser
from random import choice
from time import sleep
import string
def generate_password(length):
    lower_case = list(string.ascii_lowercase)
    upper_case = list(string.ascii_uppercase)
    simbols = ["!", "#", "$", "%", "&", "/", "(", ")", "=", "?",
                "¿", "¡", "+", "*", "{", "}", "[", "]", ":", ".",
                "-", "_"]
    characters = lower_case + upper_case + simbols
    password = ("").join([str(choice(characters)) for x in range(0, length)])
    print(password)

def get_arguments():
    parser = ArgumentParser()
    parser.add_argument("-l", "--length", dest="length",
                        type=int, default=15,
                        required=False,
                        help="The Length of the password")
    args = parser.parse_args()
    return args
    
if __name__ == "__main__":
        arguments = get_arguments()
        print("The new password is below\n\r")
        generate_password(arguments.length)
        sleep(60)
