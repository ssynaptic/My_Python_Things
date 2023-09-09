from argparse import ArgumentParser
from database import Database
class App:
    def __init__(self): 
        self.get_arguments()
        self.main()
    def main(self):
        self.databse = Database()
        self.check_db_results = self.databse.check_db_name(self.args.db_name[0])
        if self.check_db_results:
            print("Welcome to the password manager")
            self.databse.create_database(self.args.db_name[0])
            exit(code=0)
        else:
            print("That is not a valid name, enter another")
            exit(code=1)

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
if __name__ == "__main__":
    app = App()