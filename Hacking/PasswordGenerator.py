from optparse import OptionParser
from random import choice
from sys import exit
import string
def generate_password(length=15):
    lower_case = list(string.ascii_lowercase)
    upper_case = list(string.ascii_uppercase)
    simbols = ["!", "#", "$", "%", "&", "/", "(", ")", "=", "?",
                "¿", "¡", "+", "*", "{", "}", "[", "]", ":", ".",
                "-", "_"]
    characters = lower_case + upper_case + simbols
    password = "".join([str(choice(characters)) for x in range(0, length)])
    print(password)

def get_arguments():
    parser = OptionParser()
    parser.add_option("--length", dest="length",
                      default=15,
                      help="The Lenght of the Password",
                      metavar="LENGTH")
    (options, arguments) = parser.parse_args()
    return options
    
if __name__ == "__main__":
    try:
        options = get_arguments()
        if options.length == 15:
            print("""Se generara la contraseña con una longitud por
defecto de 15 caracteres""")
            password = generate_password(int(options.length))
        else:
            password = generate_password(int(options.length))
    except ValueError:
        print("""\nDebe especificar la longitud de la contraseña
con un numero entero""")
