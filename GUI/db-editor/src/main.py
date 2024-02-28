from argparse import ArgumentParser
from argparse import Namespace as argNamespace
from config import load_configuration
from typing import Any, Dict
from app import App

def get_arguments() -> argNamespace:
    parser: ArgumentParser = ArgumentParser(prog="SQLite Database Editor",
                            usage="python3 / python.exe gui.py <OPTIONS>",
                            description="",
                            epilog="")
    parser.add_argument("--config", action="store",
                        default="configuration.toml",
                        dest="config_path",
                        help="Path to the configuration file",
                        metavar="PATH",
                        nargs=1,
                        required=False)
    args: argNamespace = parser.parse_args()
    return args

if __name__ == "__main__":
    args: argNamespace = get_arguments()
    conf: Dict[str, Any] = load_configuration(args.config_path \
        if type(args.config_path) == str else args.config_path[0])
    app: App = App(configuration=conf)
    app.mainloop()